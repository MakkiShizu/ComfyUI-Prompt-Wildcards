// revise from https://github.com/TFL-TFL/ComfyUI_Text_Translation/blob/main/js/ulits.js

export const dynamic_connection = (
  node,
  index,
  connected,
  connectionPrefix = "input_",
  connectionType = "PSDLAYER"
) => {
  if (!connected && node.inputs.length > 1) {
    const stackTrace = new Error().stack;
    for (let i = node.inputs.length - 2; i >= 0; i--) {
      if (
        !stackTrace.includes("LGraphNode.prototype.connect") &&
        !stackTrace.includes("LGraphNode.connect") &&
        !stackTrace.includes("loadGraphData") &&
        !node.inputs[i].link
      ) {
        node.removeInput(i);
      }
    }
  }

  let last_slot = node.inputs[node.inputs.length - 1];
  if (last_slot.link != undefined) {
    node.addInput(`${connectionPrefix}`, connectionType);
  }

  if (connected && node.inputs.length > 1) {
    const stackTrace = new Error().stack;
    for (let i = node.inputs.length - 2; i >= 0; i--) {
      if (
        !stackTrace.includes("LGraphNode.prototype.connect") &&
        !stackTrace.includes("LGraphNode.connect") &&
        !stackTrace.includes("loadGraphData") &&
        !node.inputs[i].link
      ) {
        node.removeInput(i);
      }
    }
  }

  if (node.inputs.length > 1) {
    for (let i = 0; i < node.inputs.length - 1; i++) {
      node.inputs[i].name = `${connectionPrefix}${i + 1}`;
      node.inputs[i].label = `${connectionPrefix}${i + 1}`;
    }
  }
};
