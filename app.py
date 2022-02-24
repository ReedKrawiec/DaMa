import os
import importlib.util
import sys
import json
from PIL import Image
import random
import copy
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
    screenshot = Image.open(f"./small_input/{image}")
    for provider in config["providers"]:
        name = provider["name"]
        if random.random() < provider["probability"]:
            for _ in range(provider["min"],provider["max"]):
                position = copy.deepcopy(provider["position"])
                element = provider_creators[name]()
                if not provider["offscreen"]:
                    width, height = element["image"].size
                    position["x"]["max"] = position["x"]["max"] - width
                    position["y"]["max"] = position["y"]["max"] - height
                x = random.randrange(position["x"]["min"],position["x"]["max"])
                y = random.randrange(position["y"]["min"],position["y"]["max"])
                screenshot.paste(element["image"],(x,y))
    screenshot.save(f"{index}.png")
    print(screenshot)
