from PIL import Image, ImageDraw
import random

def create():
    width = random.randrange(100,500)
    height = random.randrange(100,500)
    output_image = Image.new("RGB", (width, height))
    annotations = [(0,width/2,height/2,width,height)]
    return {"image": output_image, "labels": annotations}