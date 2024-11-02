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
                    {"default": 1, "min": 1, "max": 10, "step": 1},
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

        for i in range(1, 10):
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


NODE_CLASS_MAPPINGS = {
    "makiwildcards": makiwildcards,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "makiwildcards": "makiwildcards",
}
