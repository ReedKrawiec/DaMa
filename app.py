import os
import importlib.util
from re import A
import sys
import json
from PIL import Image, ImageDraw
import random
import copy

DRAW_ANNOTATIONS = True

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
                image = element["image"]
                labels = element["labels"]
                if not provider["offscreen"]:
                    width, height = element["image"].size
                    position["x"]["max"] = position["x"]["max"] - 1 * width
                    position["y"]["max"] = position["y"]["max"] - 1 * height
                print(position)
                x = random.randrange(position["x"]["min"],position["x"]["max"])
                y = random.randrange(position["y"]["min"],position["y"]["max"])
                # Adjust labels to take into account position within image
                labels = list(map(lambda label: (label[0],x + label[1], y + label[2], label[3], label[4]), labels))
                screenshot.paste(image,(int(x),int(y)))
    output = config["output"]
    output_image = Image.new("RGB", (output["width"], output["height"]))
    if screenshot.size[0] > screenshot.size[1]:
        
        ratio = output["width"] / screenshot.size[0]
        gutter = (output["height"] - screenshot.size[1] * ratio) / 2
        def adjustlabel(label):
            class_index, x, y, width, height = label
            x = int(x * ratio) / output["width"]
            y = int(y * ratio + gutter) / output["height"] 
            width = int(width * ratio) / output["width"]
            height = int(height * ratio) / output["height"]
            return (class_index, x, y, width, height)
        # we resize the width to the output width, and the height is proportional
        screenshot = screenshot.resize((output["width"], int(screenshot.size[1] * ratio)))
        # adjust labels to account for the resize
        labels = list(map(adjustlabel, labels))
        print(str(labels) + " \n")
    else:
        # We resize the size to the output height, and the width is proportional
        ratio = output["height"] / screenshot.size[1]
        screenshot = screenshot.resize((int(screenshot.size[0] * ratio), output["height"]))
    output_image.paste(screenshot, (
        int((output["width"] - screenshot.size[0]) / 2), # These are the cordinates that place the image in the center of the output image
        int((output["height"] - screenshot.size[1]) / 2))
    )
    with open(f"./output/test/labels/{index}.txt","w") as f:
        classes = 20
        colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(classes)]
        print(colors)
        for label in labels:
            f.write(f"{label[0]} {label[1]} {label[2]} {label[3]} {label[4]}\n")
            if DRAW_ANNOTATIONS:
                draw = ImageDraw.Draw(output_image)
                cindex,x,y,width,height = label
                x = int(x * output["width"])
                y = int(y * output["height"])
                width = int(width * output["width"])
                height = int(height * output["height"])
                draw.rectangle([x - width/2,y - height/2,x + width/2,y + height/2], outline=colors[cindex])
            
    output_image.save(f"./output/test/images/{index}.png")
    
