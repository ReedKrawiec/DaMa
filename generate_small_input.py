from PIL import Image,ImageDraw

for i in range(100):
    im = Image.new("RGB",(2000,2000))
    draw = ImageDraw.Draw(im)
    draw.rectangle([(0,0),im.size], fill ="#ffff33")
    im.save(f"./small_input/{i}.png")