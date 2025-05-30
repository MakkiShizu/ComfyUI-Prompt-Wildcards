// revise from https://github.com/TFL-TFL/ComfyUI_Text_Translation/blob/main/js/text.js

import { app } from "../../scripts/app.js";
import { dynamic_connection } from "./utils.js";

app.registerExtension({
  name: "ComfyUI-Prompt-Wildcards.textconcatenate_v2.text",

  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    switch (nodeData.name) {
      case "textconcatenate_v2":
        text_concatenate_widget(nodeType, nodeData, app);
        break;
    }
  },
});

function text_concatenate_widget(nodeType, nodeData, app) {
  const input_name = "text";

  const originalSerialize = nodeType.prototype.serialize;
  nodeType.prototype.serialize = function () {
    const data = originalSerialize?.call(this) || {};
    data._dynamicInputs = Array.from(this._dynamicInputs || []);
    return data;
  };

  const originalConfigure = nodeType.prototype.onConfigure;
  nodeType.prototype.onConfigure = function (data) {
    this._isRestoring = true;
    this._dynamicInputs = new Set(data?._dynamicInputs || []);
    const result = originalConfigure?.call(this, data);

    dynamic_connection(this, -1, false, input_name, "STRING");

    this._isRestoring = false;
    return result;
  };

  const onNodeCreated = nodeType.prototype.onNodeCreated;
  nodeType.prototype.onNodeCreated = function () {
    const res = onNodeCreated?.apply(this, arguments);
    this.addInput(`${input_name}1`, "STRING");
    return res;
  };

  const onConnectionsChange = nodeType.prototype.onConnectionsChange;
  nodeType.prototype.onConnectionsChange = function (
    type,
    index,
    connected,
    link_info
  ) {
    if (!link_info) return;
    const res = onConnectionsChange?.apply(this, arguments);

    const connectionType = this.inputs[0]?.type || "STRING";

    dynamic_connection(this, index, connected, input_name, connectionType);

    return res;
  };
}
