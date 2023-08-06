import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';

import {
  IETCJupyterLabTelemetry,
  NotebookSaveEvent,
  CellExecutionEvent,
  NotebookScrollEvent,
  ActiveCellChangeEvent,
  NotebookOpenEvent,
  CellAddEvent,
  CellRemoveEvent
} from "@educational-technology-collective/etc_jupyterlab_telemetry_extension";

import { requestAPI } from './handler';

const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_telemetry_coursera:plugin';

export class AWSAPIGatewayAdapter {

  private _userId: Promise<string>;

  constructor() {

    this._userId = (async () => {

      try { // to get the user id.
        return await requestAPI<string>("id");
      } catch (e) {
        console.error(`Error on GET id.\n${e}`);
        return "UNDEFINED";
      }
      //  This request is specific to the Coursera environment; hence, it may not be relevant in other contexts.
      //  The request for the `id` resource will return the value of the WORKSPACE_ID environment variable that is assigned on the server.
    })();
  }

  adaptMessage(
    sender: NotebookSaveEvent | CellExecutionEvent | NotebookScrollEvent | ActiveCellChangeEvent | NotebookOpenEvent | CellAddEvent | CellRemoveEvent, 
    data: object
    ): void {

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

        //console.log(response);
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
  requires: [INotebookTracker, IETCJupyterLabTelemetry],
  activate: (
    app: JupyterFrontEnd, 
    notebookTracker: INotebookTracker, 
    etcJupyterLabTelemetry: IETCJupyterLabTelemetry
    ) => {
    console.log('JupyterLab extension @educational-technology-collective/etc_jupyterlab_telemetry_coursera is activated!');

    let messageAdapter = new AWSAPIGatewayAdapter();

    notebookTracker.widgetAdded.connect(async (sender: INotebookTracker, notebookPanel: NotebookPanel) => {

      await notebookPanel.revealed;
      await notebookPanel.sessionContext.ready;

      let notebookEvent = new etcJupyterLabTelemetry.NotebookEventLibrary({ notebookPanel });

      notebookEvent.notebookOpenEvent.notebookOpened.connect(messageAdapter.adaptMessage, messageAdapter);
      notebookEvent.notebookSaveEvent.notebookSaved.connect(messageAdapter.adaptMessage, messageAdapter);
      notebookEvent.activeCellChangeEvent.activeCellChanged.connect(messageAdapter.adaptMessage, messageAdapter);
      notebookEvent.cellAddEvent.cellAdded.connect(messageAdapter.adaptMessage, messageAdapter);
      notebookEvent.cellRemoveEvent.cellRemoved.connect(messageAdapter.adaptMessage, messageAdapter);
      notebookEvent.notebookScrollEvent.notebookScrolled.connect(messageAdapter.adaptMessage, messageAdapter);
      notebookEvent.cellExecutionEvent.cellExecuted.connect(messageAdapter.adaptMessage, messageAdapter);
    });

  }
};

export default plugin;
