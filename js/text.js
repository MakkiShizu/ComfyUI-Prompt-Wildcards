// revise from https://github.com/TFL-TFL/ComfyUI_Text_Translation/blob/main/js/text.js
import { app } from "../../scripts/app.js";
import { dynamic_connection } from "./utils.js";

app.registerExtension({
  name: "textconcatenate_v2.text",

  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    switch (nodeData.name) {
      case "textconcatenate_v2":
        text_concatenate_widget(nodeType, nodeData, app);
        break;
    }
  },
});

function text_concatenate_widget(nodeType, nodeData, app) {
  var input_name = "text";

  const onNodeCreated = nodeType.prototype.onNodeCreated;
  nodeType.prototype.onNodeCreated = function () {
    const onc = onNodeCreated?.apply(this, arguments);
    this.addInput(`${input_name}`, "STRING");
    return onc;
  };

  const onConnectionsChange = nodeType.prototype.onConnectionsChange;
  nodeType.prototype.onConnectionsChange = function (
    type,
    index,
    connected,
    link_info
  ) {
    if (!link_info) return;

    const occ = onConnectionsChange
      ? onConnectionsChange.apply(this, arguments)
      : undefined;

    const connectionType =
      this.inputs.length > 0 ? this.inputs[0].type : "STRING";
    dynamic_connection(
      this,
      index,
      connected,
      input_name,
      this.inputs[0].type,
      connectionType
    );
    return occ;
  };
}
