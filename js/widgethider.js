// revise from https://github.com/jags111/efficiency-nodes-comfyui/blob/main/js/widgethider.js
import { app } from "../../scripts/app.js";

let origProps = {};

const findWidgetByName = (node, name) => {
  return node.widgets ? node.widgets.find((w) => w.name === name) : null;
};

const doesInputWithNameExist = (node, name) => {
  return node.inputs ? node.inputs.some((input) => input.name === name) : false;
};

const HIDDEN_TAG = "tschide";

function toggleWidget(node, widget, show = false, suffix = "") {
  if (!widget || doesInputWithNameExist(node, widget.name)) return;

  if (!origProps[widget.name]) {
    origProps[widget.name] = {
      origType: widget.type,
      origComputeSize: widget.computeSize,
    };
  }

  widget.type = show ? origProps[widget.name].origType : HIDDEN_TAG + suffix;
  widget.computeSize = show
    ? origProps[widget.name].origComputeSize
    : () => [0, -4];
  widget.linkedWidgets?.forEach((w) =>
    toggleWidget(node, w, ":" + widget.name, show)
  );

  const newHeight = node.computeSize()[1];

  node.setSize([node.size[0], newHeight]);
}

function handleVisibility(node, countValue, node_type) {
  const baseNamesMap = {
    makiwildcards: ["wildcard_name"],
  };

  const baseNames = baseNamesMap[node_type];

  for (let i = 1; i <= 50; i++) {
    const nameWidget = findWidgetByName(node, `${baseNames[0]}_${i}`);

    if (i <= countValue) {
      toggleWidget(node, nameWidget, true);
      if (node_type === "makiwildcards") {
        toggleWidget(node, nameWidget, true);
      }
    } else {
      toggleWidget(node, nameWidget, false);
    }
  }
}

const nodeWidgetHandlers = {
  makiwildcards: {
    wildcards_count: handlewildcards,
  },
};

function widgetLogic(node, widget) {
  const handler = nodeWidgetHandlers[node.comfyClass]?.[widget.name];

  if (handler) {
    handler(node, widget);
  }
}

function handlewildcards(node, widget) {
  handleVisibility(node, widget.value, "makiwildcards");
}

app.registerExtension({
  name: "wildcards.widgethider",
  nodeCreated(node) {
    for (const w of node.widgets || []) {
      let widgetValue = w.value;
      let originalDescriptor = Object.getOwnPropertyDescriptor(w, "value");
      if (!originalDescriptor) {
        originalDescriptor = Object.getOwnPropertyDescriptor(
          w.constructor.prototype,
          "value"
        );
      }
      widgetLogic(node, w);
      Object.defineProperty(w, "value", {
        get() {
          let valueToReturn =
            originalDescriptor && originalDescriptor.get
              ? originalDescriptor.get.call(w)
              : widgetValue;

          return valueToReturn;
        },
        set(newVal) {
          if (originalDescriptor && originalDescriptor.set) {
            originalDescriptor.set.call(w, newVal);
          } else {
            widgetValue = newVal;
          }
          widgetLogic(node, w);
        },
      });
    }
    setTimeout(() => {
      initialized = true;
    }, 500);
    // alert("wildcards test");
  },
});
