import json
from fenToBoardImage import fenToImage, loadPiecesFolder
import random

class board:
  def config(self,image):
    size = random.randrange(0,800)
    theme = random.randrange(0,5)
    piece_theme = random.randrange(0,5)
    return {
      "name":"board",
      "config":{
        "board_theme":theme,
        "piece_theme":piece_theme,
        "size":{
          "width":size,
          "height":size
        }
      },
      "positions":{
        "x":{
          "min":0,
          "max":image["width"] - size
        },
        "y":{
          "min":0,
          "max":image["height"] - size
        }
      }  
    }
  def create():
    pass

b = board()
config = json.dumps(b.config({
  "width":1920,
  "height":1080,
}))
print(config)