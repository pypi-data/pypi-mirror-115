
import json
from pathlib import Path

from ._version import __version__

HERE = Path(__file__).parent.resolve()

with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": data["name"]
    }]

# from .handlers import setup_handlers
from .handlers import ETCJupyterLabTelemetryCoursera

def _jupyter_server_extension_points():
    return [{
        "module": "etc_jupyterlab_telemetry_coursera",
         "app": ETCJupyterLabTelemetryCoursera
    }]

# For backward compatibility with notebook server - useful for Binder/JupyterHub
load_jupyter_server_extension = ETCJupyterLabTelemetryCoursera.load_classic_server_extension
