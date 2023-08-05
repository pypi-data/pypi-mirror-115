import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { INotebookEvent } from "@educational-technology-collective/etc_jupyterlab_telemetry_extension";

import { requestAPI } from './handler';

const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_telemetry_coursera:plugin';

export class AWSAPIGatewayAdapter {

  private _userId: Promise<string>;

  constructor() {

    this._userId = (async () => {


      try { // to get the user id.
        return await requestAPI<string>("id");
      } catch (e) {
        console.error(`Error on GET /etc_jupyterlab_telemetry/id}.\n${e}`);
        return "UNDEFINED";
      }
      //  This request is specific to the Coursera environment; hence, it may not be relevant in other contexts.
      //  The request for the `id` resource will return the value of the WORKSPACE_ID environment variable that is assigned on the server.
    })();
  }

  adaptMessage(sender: any, data: any): void {

    (async () => {
      try {

        //
        data = {
          ...data,
          ...{
            user_id: await this._userId
          }
        }
        //  The user id is not a characteristic of the event; hence, it is added late. 

        console.log(data);

        let response = await requestAPI<string>("s3", { method: "POST", body: JSON.stringify(data) });
        console.log(response);
      }
      catch (e) {
        console.error(e);
      }
    })();
  }
}

/**
 * Initialization data for the @educational-technology-collective/etc_jupyterlab_telemetry_coursera extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [INotebookEvent],
  activate: (app: JupyterFrontEnd, notebookEvent: INotebookEvent) => {
    console.log('JupyterLab extension @educational-technology-collective/etc_jupyterlab_telemetry_coursera is activated!');

    let messageAdapter = new AWSAPIGatewayAdapter();

    notebookEvent.notebookSaved.connect(messageAdapter.adaptMessage, messageAdapter);
    notebookEvent.activeCellChanged.connect(messageAdapter.adaptMessage, messageAdapter);
    notebookEvent.cellAdded.connect(messageAdapter.adaptMessage, messageAdapter);
    notebookEvent.cellExecuted.connect(messageAdapter.adaptMessage, messageAdapter);
    notebookEvent.cellRemoved.connect(messageAdapter.adaptMessage, messageAdapter);
    notebookEvent.notebookOpened.connect(messageAdapter.adaptMessage, messageAdapter);
    notebookEvent.notebookScrolled.connect(messageAdapter.adaptMessage, messageAdapter);
  }
};

export default plugin;
