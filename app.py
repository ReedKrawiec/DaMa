import os
import importlib.util
import sys
import json

with open("dama.json", "r") as f:
    config = json.loads(f.read())

provider_creators = {}

for provider_name in os.listdir("./providers"):
    spec = importlib.util.spec_from_file_location(
        "definition", f"./providers/{provider_name}/def.py"
    )
    provider = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(provider)
    provider_creators[provider_name] = provider.create

images = os.listdir("./small_input")

for index, image in enumerate(images):
    board = provider_creators["board"]()["image"]
    board.save(f"test{index}.png")
