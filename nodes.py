import os
import random

from pathlib import Path

wildcards_dir = Path(__file__).parent / "wildcards"
os.makedirs(wildcards_dir, exist_ok=True)
print(f"Using wildcards dir: {wildcards_dir}")

WILDCARDS_LIST = ["None"] + [
    str(wildcard.relative_to(wildcards_dir))[:-4]
    for wildcard in wildcards_dir.rglob("*.txt")
]


class makiwildcards:
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "wildcards_count": (
                    "INT",
                    {"default": 3, "min": 1, "max": 50, "step": 1},
                ),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
            },
            "optional": {
                "text": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                    },
                ),
            },
        }

        for i in range(1, 50):
            inputs["required"][f"wildcard_name_{i}"] = (
                WILDCARDS_LIST,
                {"default": WILDCARDS_LIST[0]},
            )

        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "makiwildcards"
    CATEGORY = "utils"

    def makiwildcards(self, wildcards_count, seed, text=None, **kwargs):

        selected_wildcards = [
            kwargs[f"wildcard_name_{i}"] for i in range(1, wildcards_count + 1)
        ]
        results = []

        for root, dirs, files in os.walk(wildcards_dir):
            for wildcard in selected_wildcards:
                wildcard_file = Path(root) / f"{wildcard}.txt"
                if wildcard_file.is_file():
                    with open(wildcard_file, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        if lines:
                            random.seed(seed)
                            random_line = random.choice(lines).strip()
                            results.append(random_line)
                else:
                    print(f"Wildcard File not found: {wildcard_file}")

            joined_result = ", ".join(results)
            print(f"wildcards:{joined_result} ||| seed:{seed}")

            if text is not None:
                joined_result = f"{text},{joined_result}"
            return (joined_result,)


# textconcatenate is revise from https://github.com/WASasquatch/was-node-suite-comfyui/blob/main/WAS_Node_Suite.py#L10311-L10362 2024/12/07
class textconcatenate:
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "text_count": (
                    "INT",
                    {"default": 3, "min": 1, "max": 50, "step": 1},
                ),
                "delimiter": ("STRING", {"default": ", "}),
                "clean_whitespace": ("BOOLEAN", {"default": True}),
                "replace_underscore": ("BOOLEAN", {"default": True}),
            },
        }

        for i in range(1, 50):
            inputs["required"][f"text_{i}"] = (
                "STRING",
                {"default": ""},
            )

        return inputs

    RETURN_TYPES = ("STRING",)
    FUNCTION = "text_concatenate"

    CATEGORY = "utils"

    def text_concatenate(
        self, text_count, delimiter, clean_whitespace, replace_underscore, **kwargs
    ):
        text_inputs = []
        selected_texts = [kwargs[f"text_{i}"] for i in range(1, text_count + 1)]

        for text in selected_texts:
            if clean_whitespace:
                text = text.strip()

            if replace_underscore:
                text = text.replace("_", " ")

            if text != "":
                text_inputs.append(text)

        if delimiter in ("\n", "\\n"):
            delimiter = "\n"

        merged_text = delimiter.join(text_inputs)

        return (merged_text,)


NODE_CLASS_MAPPINGS = {
    "makiwildcards": makiwildcards,
    "textconcatenate": textconcatenate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "makiwildcards": "makiwildcards",
    "textconcatenate": "textconcatenate",
}
