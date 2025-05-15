import os
import random
import yaml
import folder_paths

from pathlib import Path
from .logging import logger
from yaml import Loader

wildcards_dir = Path(__file__).parent / "wildcards"
os.makedirs(wildcards_dir, exist_ok=True)
wildcards_base_dir = Path(folder_paths.base_path) / "wildcards"
# os.makedirs(wildcards_base_dir, exist_ok=True)
logger.info(f"Using wildcards dir:☯️{wildcards_dir} と {wildcards_base_dir}☯️")

full_dirs = [wildcards_dir, wildcards_base_dir]


def merge_duplicate_keys(constructor, node):
    data = {}
    for key_node, value_node in node.value:
        key = constructor.construct_object(key_node)
        value = constructor.construct_object(value_node)
        if key in data:
            if isinstance(data[key], list):
                data[key].extend(value if isinstance(value, list) else [value])
            else:
                data[key] = [data[key]] + (
                    value if isinstance(value, list) else [value]
                )
        else:
            data[key] = value if isinstance(value, list) else [value]
    return data


Loader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, merge_duplicate_keys
)

WILDCARDS_LIST = ["None"]

for wildcard in wildcards_dir.rglob("*"):
    if wildcard.suffix.lower() in (".txt", ".yaml", ".yml"):
        relative_path = str(wildcard.relative_to(wildcards_dir)).replace("\\", "/")
        if wildcard.suffix.lower() in (".yaml", ".yml"):
            base = f"custom_nodes | {relative_path}"
        else:
            base = f"custom_nodes | {relative_path[:-len(wildcard.suffix)]}"
        WILDCARDS_LIST.append(base)
        if wildcard.suffix.lower() in (".yaml", ".yml"):
            with open(wildcard, "r", encoding="utf-8") as f:
                try:
                    data = yaml.load(f, Loader=Loader)

                    def dfs(node, path):
                        if isinstance(node, dict):
                            for k, v in node.items():
                                new_path = path + [k]
                                WILDCARDS_LIST.append(
                                    f"{base} | {' | '.join(new_path)}"
                                )
                                dfs(v, new_path)
                        elif isinstance(node, list):
                            for item in node:
                                dfs(item, path)

                    dfs(data, [])
                except Exception as e:
                    logger.warning(f"Error processing {wildcard}: {e}")

for wildcard in wildcards_base_dir.rglob("*"):
    if wildcard.suffix.lower() in (".txt", ".yaml", ".yml"):
        relative_path = str(wildcard.relative_to(wildcards_base_dir)).replace("\\", "/")
        if wildcard.suffix.lower() in (".yaml", ".yml"):
            base = f"base_path | {relative_path}"
        else:
            base = f"base_path | {relative_path[:-len(wildcard.suffix)]}"
        WILDCARDS_LIST.append(base)
        if wildcard.suffix.lower() in (".yaml", ".yml"):
            with open(wildcard, "r", encoding="utf-8") as f:
                try:
                    data = yaml.load(f, Loader=Loader)

                    def dfs(node, path):
                        if isinstance(node, dict):
                            for k, v in node.items():
                                new_path = path + [k]
                                WILDCARDS_LIST.append(
                                    f"{base} | {' | '.join(new_path)}"
                                )
                                dfs(v, new_path)
                        elif isinstance(node, list):
                            for item in node:
                                dfs(item, path)

                    dfs(data, [])
                except Exception as e:
                    logger.warning(f"Error processing {wildcard}: {e}")


class makiwildcards:
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "wildcards_count": (
                    "INT",
                    {"default": 3, "min": 1, "max": 50, "step": 1},
                ),
                "delimiter": ("STRING", {"default": ", "}),
                "clean_whitespace": ("BOOLEAN", {"default": True}),
                "replace_underscore": ("BOOLEAN", {"default": True}),
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

    def makiwildcards(
        self,
        wildcards_count,
        delimiter,
        clean_whitespace,
        replace_underscore,
        randoms,
        seed,
        text=None,
        **kwargs,
    ):

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
                        parts = wildcard.split(" | ")

                        if parts[0] == "custom_nodes":
                            file_path_part = parts[1]
                            internal_path = parts[2:]
                            target_dir = wildcards_dir
                        elif parts[0] == "base_path":
                            file_path_part = parts[1]
                            internal_path = parts[2:]
                            target_dir = wildcards_base_dir
                        else:
                            continue

                        yaml_file = target_dir / file_path_part
                        if not yaml_file.exists():
                            yaml_file = yaml_file.with_suffix(".yml")
                        txt_file = target_dir / f"{file_path_part}.txt"

                        if yaml_file.exists():
                            file_type = "yaml"
                            wildcard_file = yaml_file
                        elif txt_file.exists():
                            file_type = "txt"
                            wildcard_file = txt_file
                        else:
                            logger.warning(f"Wildcard file not found: {file_path_part}")
                            continue

                        with open(wildcard_file, "r", encoding="utf-8") as f:
                            raw_content = f.read()
                            f.seek(0)
                            if file_type == "yaml":
                                try:
                                    data = yaml.load(f, Loader=Loader)
                                    current_data = data

                                    for key in internal_path:
                                        if isinstance(current_data, dict):
                                            current_data = current_data.get(key, {})
                                        elif isinstance(current_data, list):
                                            collected = []
                                            for item in current_data:
                                                if isinstance(item, dict):
                                                    if key in item:
                                                        collected.append(item[key])
                                                    elif str(key).isdigit() and int(
                                                        key
                                                    ) < len(item):
                                                        collected.append(item[int(key)])
                                            current_data = collected
                                        else:
                                            current_data = []
                                            break

                                    def collect_lines(node):
                                        lines = []
                                        if isinstance(node, list):
                                            for item in node:
                                                lines.extend(collect_lines(item))
                                        elif isinstance(node, dict):
                                            for v in node.values():
                                                lines.extend(collect_lines(v))
                                        elif isinstance(node, str):
                                            cleaned = (
                                                node.strip()
                                                .replace("\r\n", "\n")
                                                .split("\n")
                                            )
                                            lines.extend(
                                                [
                                                    line.strip()
                                                    for line in cleaned
                                                    if line.strip()
                                                ]
                                            )
                                        return lines

                                    lines = collect_lines(current_data)
                                    lines = [
                                        line for line in lines if isinstance(line, str)
                                    ]

                                except Exception as e:
                                    logger.warning(f"YAML error: {e}")
                                    continue
                            else:
                                lines = raw_content.splitlines()
                        if lines:
                            file_entry = (
                                f"File: {file_path_part}\n"
                                f"Content:\n{raw_content}\n-----\n"
                            )
                            file_contents.append(file_entry)
                            if randoms:
                                random.seed(seed + index)
                                random_line = random.choice(lines)
                                if clean_whitespace:
                                    random_line = random_line.strip()
                                if replace_underscore:
                                    random_line = random_line.replace("_", " ")
                                results.append(random_line)
                            else:
                                selected_line_index = seed - 1
                                selected_line_index %= len(lines)
                                selected_line = lines[selected_line_index]
                                if clean_whitespace:
                                    selected_line = selected_line.strip()
                                if replace_underscore:
                                    selected_line = selected_line.replace("_", " ")
                                results.append(selected_line)

                if delimiter in ("\n", "\\n"):
                    delimiter = "\n"

                joined_result = delimiter.join(results)
                logger.info(f"wildcards:{joined_result} ||| seed:{seed}")

                if text == "":
                    joined_result = f"{joined_result}"
                else:
                    joined_result = f"{text}{delimiter}{joined_result}"
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
