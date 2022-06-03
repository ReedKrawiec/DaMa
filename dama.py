import os
import importlib.util
from re import A
import sys
import json
from PIL import Image, ImageDraw
import random
import copy
from multiprocessing import Pool

PROCESSES = 8

DRAW_LABELS = "--draw-labels" in sys.argv

if "--config" in sys.argv:
    config_name = sys.argv[sys.argv.index("--config") + 1]
else:
    config_name = "dama.json"

with open(config_name, "r") as f:
    config = json.loads(f.read())

output_path = config["output"]["path"]

provider_creators = {}

for provider_name in os.listdir("./providers"):
    spec = importlib.util.spec_from_file_location(
        "definition", f"./providers/{provider_name}/def.py"
    )
    provider = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(provider)
    provider_creators[provider_name] = provider.create

input_dir = config["input"]
images = os.listdir(input_dir)
#checks if two rectangles intersect with format (x,y,width, height)
# x,y,width,height
def squareIntersects(one,two):
    x1,x2 = one[0] - one[2]/2, one[0] + one[2]/2
    x3,x4 = two[0] - two[2]/2, two[0] + two[2]/2
    y1,y2 = one[1] - one[3]/2, one[1] + one[3]/2
    y3,y4 = two[1] - two[3]/2, two[1] + two[3]/2
    if x1 > x3 and x1 < x4:
        if y1 > y3 and y1 < y4:
            return True
        if y2 > y3 and y2 < y4:
            return True
        if y1 < y3 and y2 > y4:
            return True
    if x2 > x3 and x2 < x4:
        if y1 > y3 and y1 < y4:
            return True
        if y2 > y3 and y2 < y4:
            return True
        if y1 < y3 and y2 > y4:
            return True
    return False

def generate(provider):
    name = provider["name"]
    position = copy.deepcopy(provider["position"])
    element = provider_creators[name]()
    image = element["image"]
    labels = element["labels"]
    if not provider["offscreen"]:
        width, height = element["image"].size
        position["x"]["max"] = position["x"]["max"] - 1 * width
        position["y"]["max"] = position["y"]["max"] - 1 * height
    return image, labels, width, height, position
output = config["output"]
distribution = list(output["distribution"].keys())

def process(inp):
    i, images = inp
    current_group = 0
    percent = output["distribution"][distribution[current_group]]
    offsets = 0
    for index, image in enumerate(images):
        print("Working on: " + image)
        screenshot = Image.open(f"{input_dir}/{image}")
        class_list = []
        full_labels = []
        placements = []
        for provider in config["providers"]:
            if random.random() < provider["probability"]:
                for _ in range(provider["min"],provider["max"]):
                    image, labels, width, height, position = generate(provider)
                    counter = 0
                    if not provider["overlap"]:
                        valid = False
                        while not valid:
                            x = random.randrange(position["x"]["min"],position["x"]["max"])
                            y = random.randrange(position["y"]["min"],position["y"]["max"])
                            valid = True
                            for placement in placements:
                                if squareIntersects((x,y,width,height),placement):
                                    valid = False
                            counter += 1
                            if counter > 100:
                                image, labels, width, height, position = generate(provider)
                            if counter > 200:
                                break
                    placements.append((x,y,width,height))
                    # Adjust labels to take into account position within image
                    labels = list(map(lambda label: (label[0] + len(class_list),x + label[1], y + label[2], label[3], label[4]), labels))
                    full_labels.extend(labels)
                    screenshot.paste(image,(int(x),int(y)))
            class_list.extend(provider["classes"])
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
            full_labels = list(map(adjustlabel, full_labels))
            
        else:
            # We resize the size to the output height, and the width is proportional
            ratio = output["height"] / screenshot.size[1]
            screenshot = screenshot.resize((int(screenshot.size[0] * ratio), output["height"]))
        output_image.paste(screenshot, (
            int((output["width"] - screenshot.size[0]) / 2), # These are the cordinates that place the image in the center of the output image
            int((output["height"] - screenshot.size[1]) / 2))
        )
        folder = distribution[current_group]
        
        with open(f"{output_path}/{folder}/labels/{int(index + i)}.txt","w") as f:
            classes = len(class_list)
            colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                for i in range(classes)]
            for label in full_labels:
                f.write(f"{label[0]} {label[1]} {label[2]} {label[3]} {label[4]}\n")
                if DRAW_LABELS:
                    draw = ImageDraw.Draw(output_image)
                    cindex,_x,_y,width,height = label
                    _x = int(_x * output["width"])
                    _y = int(_y * output["height"])
                    
                    width = int(width * output["width"])
                    height = int(height * output["height"])
                    draw.rectangle([_x - width/2,_y - height/2,_x + width/2,_y + height/2], outline=colors[cindex])
        output_image.save(f"{output_path}/{folder}/images/{int(index + i)}.png")    
        if index > percent * len(images)+ offsets:
            offsets += int(index)
            current_group += 1
            percent = output["distribution"][distribution[current_group]]
            if current_group > len(distribution):
                break
if __name__ == "__main__":
    all_images = list(images)
    providers = config["providers"]
    distributions = config["output"]["distribution"]
    class_list = [y for x in providers for y in x["classes"]]
    
    for _distribution in distributions.keys():
        os.makedirs(f"{output_path}/{_distribution}/images", exist_ok=True)
        os.makedirs(f"{output_path}/{_distribution}/labels", exist_ok=True)

    with open(f"{output_path}/classes.txt","w") as f:
            for class_name in class_list:
                f.write(f"{class_name}\n")
            
    with open(f"{output_path}/data.yaml","w") as f:
        for dist in _distribution:
            f.write(f"{dist}: ../{dist}/images\n")
        f.write("\n")
        f.write(f"nc: {len(class_list)}\n")
        f.write(f"names: {str(class_list)}")
    
    

    with Pool(PROCESSES) as p:
        p.map(process, [(i * len(all_images)/PROCESSES,all_images[i::PROCESSES]) for i in range(PROCESSES)])
