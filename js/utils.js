// revise from https://github.com/TFL-TFL/ComfyUI_Text_Translation/blob/main/js/ulits.js

export const dynamic_connection = (
  node,
  index,
  connected,
  connectionPrefix = "input_",
  connectionType = "STRING"
) => {
  const removeUnusedInputs = () => {
    for (let i = node.inputs.length - 2; i >= 0; i--) {
      const input = node.inputs[i];
      if (!input.link && !input.__keepOnLoad) {
        node.removeInput(i);
      }
    }
  };

  removeUnusedInputs();

  const lastInput = node.inputs[node.inputs.length - 1];
  if (lastInput?.link) {
    const newIndex = node.inputs.length;
    const newInput = node.addInput(
      `${connectionPrefix}${newIndex}`,
      connectionType
    );
    newInput.__keepOnLoad = true;
  }

  node.inputs.forEach((input, i) => {
    input.name = `${connectionPrefix}${i + 1}`;
    input.label = input.name;
  });
};
