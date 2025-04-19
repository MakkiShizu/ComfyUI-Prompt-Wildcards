import os
import random

from pathlib import Path
import folder_paths
from .logging import logger

wildcards_dir = Path(__file__).parent / "wildcards"
os.makedirs(wildcards_dir, exist_ok=True)
wildcards_dirr = Path(folder_paths.base_path) / "wildcards"
# os.makedirs(wildcards_dirr, exist_ok=True)
logger.info(f"Using wildcards dir:☯️{wildcards_dir} と {wildcards_dirr}☯️")

full_dirs = [wildcards_dir, wildcards_dirr]

WILDCARDS_LIST = (
    ["None"]
    + [
        "custom_nodes | " + str(wildcard.relative_to(wildcards_dir))[:-4]
        for wildcard in wildcards_dir.rglob("*.txt")
    ]
    + [
        "base_path | " + str(wildcard.relative_to(wildcards_dirr))[:-4]
        for wildcard in wildcards_dirr.rglob("*.txt")
    ]
)


class makiwildcards:
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "wildcards_count": (
                    "INT",
                    {"default": 3, "min": 1, "max": 50, "step": 1},
                ),
                "randoms": ("BOOLEAN", {"default": True}),
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

    RETURN_TYPES = (
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "text",
        "file contents",
    )
    FUNCTION = "makiwildcards"
    CATEGORY = "utils/Prompt-Wildcards"

    def makiwildcards(self, wildcards_count, randoms, seed, text=None, **kwargs):

        selected_wildcards = [
            kwargs[f"wildcard_name_{i}"] for i in range(1, wildcards_count + 1)
        ]
        results = []
        file_contents = []

        for full_dir in full_dirs:
            for root, dirs, files in os.walk(full_dir):
                for index, wildcard in enumerate(selected_wildcards):
                    if wildcard == "None":
                        continue
                    else:
                        target_dir = None
                        if wildcard.startswith("custom_nodes | "):
                            wildcard_filename = wildcard[len("custom_nodes | ") :]
                            target_dir = wildcards_dir
                        if wildcard.startswith("base_path | "):
                            wildcard_filename = wildcard[len("base_path | ") :]
                            target_dir = wildcards_dirr
                        if target_dir:
                            wildcard_file = (
                                Path(target_dir) / f"{wildcard_filename}.txt"
                            )
                            if wildcard_file.is_file():
                                with open(wildcard_file, "r", encoding="utf-8") as f:
                                    raw_content = f.read()
                                    lines = raw_content.splitlines()
                                    if lines:
                                        file_entry = (
                                            f"File: {wildcard_filename}\n"
                                            f"Content:\n{raw_content}\n-----\n"
                                        )
                                        file_contents.append(file_entry)
                                        if randoms:
                                            random.seed(seed + index)
                                            random_line = random.choice(lines).strip()
                                            results.append(random_line)
                                        else:
                                            selected_line_index = seed - 1
                                            selected_line_index %= len(lines)
                                            selected_line = lines[
                                                selected_line_index
                                            ].strip()
                                            results.append(selected_line)
                            else:
                                logger.warning(
                                    f"Wildcard File not found: {wildcard_file}"
                                )

                joined_result = ", ".join(results)
                logger.info(f"wildcards:{joined_result} ||| seed:{seed}")

                if text == "":
                    joined_result = f"{joined_result}"
                else:
                    joined_result = f"{text},{joined_result}"
                return (joined_result, file_contents)


class makitextwildcards:
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "randoms": ("BOOLEAN", {"default": True}),
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

        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "makitextwildcards"
    CATEGORY = "utils/Prompt-Wildcards"

    def makitextwildcards(self, randoms, seed, text):
        lines = text.splitlines()
        if not lines:
            return ("",)

        if randoms:
            random.seed(seed)
            selected_line = random.choice(lines).strip()
        else:
            selected_line_index = (seed - 1) % len(lines)
            selected_line = lines[selected_line_index].strip()
        return (selected_line,)


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
    RETURN_NAMES = ("text",)
    FUNCTION = "text_concatenate"

    CATEGORY = "utils/Prompt-Wildcards"

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


class textconcatenate_v2:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "delimiter": ("STRING", {"default": ", "}),
                "clean_whitespace": ("BOOLEAN", {"default": True}),
                "replace_underscore": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "text_concatenate_v2"

    CATEGORY = "utils/Prompt-Wildcards"

    def text_concatenate_v2(
        self, delimiter, clean_whitespace, replace_underscore, **kwargs
    ):
        text_inputs = []
        text = ""

        for key, text in kwargs.items():
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
    "makitextwildcards": makitextwildcards,
    "textconcatenate": textconcatenate,
    "textconcatenate_v2": textconcatenate_v2,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "makiwildcards": "makiwildcards",
    "makitextwildcards": "makitextwildcards",
    "textconcatenate": "textconcatenate",
    "textconcatenate_v2": "textconcatenate_v2",
}
