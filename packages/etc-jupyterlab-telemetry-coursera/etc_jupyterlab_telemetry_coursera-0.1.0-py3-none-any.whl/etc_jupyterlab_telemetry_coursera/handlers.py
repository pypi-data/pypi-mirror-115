import os, tornado, json
from jupyter_server.extension.application import ExtensionApp
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin
from jupyter_server.utils import url_path_join
from requests import Request, Session
from traitlets.traitlets import Bool, Dict, Integer, Unicode 
import concurrent

class RouteHandler(ExtensionHandlerMixin, JupyterHandler):
    
    executor = concurrent.futures.ThreadPoolExecutor(5) 
    
    @tornado.web.authenticated
    def get(self, resource):
        if resource == 'id':
            self.finish(
                json.dumps(
                    os.getenv('WORKSPACE_ID') if os.getenv('WORKSPACE_ID') is not None else 'UNDEFINED'
                    )
                )

    @tornado.web.authenticated
    @tornado.gen.coroutine 
    def post(self, resource):
        if resource == 's3':
            result = yield self.process_request() 
            self.finish(result)
        
    @tornado.concurrent.run_on_executor 
    def process_request(self): 

        data = self.request.body
        #  This should be encoded as UTF-8.

        url = self.config['url']
        bucket = self.config['bucket']
        path = self.config['path']

        url =  url_path_join(url, bucket, path)

        with Session() as s:

            headers = {
                'Content-Type': 'application/json'
            }

            req = Request('POST', url, data=data, headers=headers)

            prepped = s.prepare_request(req)

            res = s.send(prepped)

            return json.dumps({'url': res.url, 'status_code': res.status_code})

class ETCJupyterLabTelemetryCoursera(ExtensionApp):

    # -------------- Required traits --------------
    name = 'etc_jupyterlab_telemetry_coursera'
    default_url = '/etc-jupyterlab-telemetry-coursera'
    load_other_extensions = True
    file_url_prefix = '/render'

    # --- ExtensionApp traits you can configure ---
    # static_paths = []
    # template_paths = []
    # settings = {}
    # handlers = []

    # ----------- add custom traits below ---------

    url = Unicode().tag(config=True)
    bucket = Unicode().tag(config=True)
    path = Unicode().tag(config=True)

    # `jupyter_etc_jupyterlab_telemetry_coursera_config.json`
    # {
    # "ETCJupyterLabTelemetryCoursera": {
    #   "url": "https://example.com",
    #   "bucket": "the-name-of-the-bucket",
    #   "path": "the-path"

    #     }
    # }
    #  This is what a sample configuration file looks like.
    #  This file should be placed in one of the config directories given by jupyter --paths.
    #  It must be named `jupyter_etc_jupyterlab_telemetry_coursera_config.json`.

    def initialize_settings(self):
        pass
        # Update the self.settings trait to pass extra
        # settings to the underlying Tornado Web Application.
        # self.settings.update({'<trait>':...})

    def initialize_handlers(self):
        # Extend the self.handlers trait
        base_url = self.settings['base_url']
        route_pattern = url_path_join(base_url, 'etc-jupyterlab-telemetry-coursera', '(.*)')
        handlers = [(route_pattern, RouteHandler)]
        self.handlers.extend(handlers)

    def initialize_templates(self):
        pass
        # Change the jinja templating environment

    async def stop_extension(self):
        pass
        # Perform any required shut down steps