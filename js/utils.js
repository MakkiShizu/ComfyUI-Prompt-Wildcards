// revise from https://github.com/TFL-TFL/ComfyUI_Text_Translation/blob/main/js/ulits.js

export const dynamic_connection = (
  node,
  index,
  connected,
  connectionPrefix = "input_",
  connectionType = "STRING"
) => {
  if (!node._isRestoring) {
    node._dynamicInputs = new Set();
  }

  const removeUnusedInputs = () => {
    for (let i = node.inputs.length - 1; i >= 0; i--) {
      const input = node.inputs[i];
      const isDynamic = node._dynamicInputs?.has(input.name);

      if (input.link || (isDynamic && node._isRestoring)) {
        continue;
      }

      if (isDynamic) {
        node.removeInput(i);
        node._dynamicInputs.delete(input.name);
      }
    }
  };

  const prevRestoring = node._isRestoring;
  if (node._isRestoring) {
    node._dynamicInputs = new Set(
      node.inputs
        .filter((input) => input.name.startsWith(connectionPrefix))
        .map((input) => input.name)
    );
  }

  removeUnusedInputs();

  const lastInput = node.inputs[node.inputs.length - 1];
  if (lastInput?.link && !node._isRestoring) {
    const newIndex = node.inputs.length + 1;
    const newName = `${connectionPrefix}${newIndex}`;
    const newInput = node.addInput(newName, connectionType);
    node._dynamicInputs.add(newName);
  }

  let validIndex = 1;
  node.inputs.forEach((input) => {
    if (input.name.startsWith(connectionPrefix)) {
      input.name = `${connectionPrefix}${validIndex++}`;
      input.label = input.name;
    }
  });

  node._isRestoring = prevRestoring;
};
