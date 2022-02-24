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

images = os.listdir("./input")

for index, image in enumerate(images):
    pass

print(len(images))
