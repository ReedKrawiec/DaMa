import json
from fentoboardimage import fenToImage, loadPiecesFolder, loadArrows
import random
from random import randint, choice, randrange
PGN_LOCATION = "/home/reed/Github/DataMake/providers/board/lichess_db_standard_rated_2013-01.pgn"
SETS = ["/home/reed/Github/DataMake/providers/board/pieces"]
ARROW_SETS = ["/home/reed/Github/DataMake/providers/board/arrows1"]
COLORS = [
    (),(),
]

def random_arrow_cordinates():
    KNIGHTS = [
        (2,1),
        (2,-1),
        (1,2),
        (1,-2),
        (-1,2),
        (-1,-2),
        (-2,1),
        (-2,-1),
    ]
    
    arrows = []
    
    for i in range(randrange(0,10)):
        arrow_type = randrange(0,6)
        if arrow_type == 0:
            offset = choice(KNIGHTS)
            start = (randrange(0,8), randrange(0,8))
            arrows.append((start[0]+offset[0], start[1]+offset[1]))
        elif arrow_type == 1:
            pass
        elif arrow_type == 2:
            pass
        elif arrow_type == 3:
            pass
        elif arrow_type == 4:
            pass
        elif arrow_type == 5:
            pass
        


def create():
    size = randrange(0, 800)
    theme = choice(COLORS)
    arrows = fenToImage(
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        squarelength=size / 8,
        pieceSet=loadPiecesFolder(choice(SETS)),
        darkColor=theme[0][1],
        lightColor=theme[0][0],
        flipped=choice([True, False]),
        lastMove={
            "before": (randrange(0,8), randrange(0,8)),
            "after": (randrange(0,8), randrange(0,8)),
            "darkColor": theme[1][1],
            "lightColor": theme[1][0],
        },
        ArrowSet=loadArrows(choice(ARROW_SETS)),
        Arrows=[
            ((3, 3), (1, 4)),
            ((3, 3), (2, 5)),
            ((3, 3), (4, 5)),
            ((3, 3), (5, 4)),
            ((3, 3), (5, 2)),
            ((3, 3), (4, 1)),
            ((3, 3), (2, 1)),
            ((3, 3), (1, 2)),
        ],
    )
    return {"image": arrows, "annotations": None}
