import json
from fentoboardimage import fenToImage, loadPiecesFolder, loadArrows
import random
from random import randint, choice, randrange
import chess.pgn

PGN_LOCATION = "/common/home/rbk70/projects/DataMake/providers/board/lichess_db_standard_rated_2013-01.pgn"
SETS = [
        "/common/home/rbk70/projects/DataMake/providers/board/pieces"
       ]
ARROW_SETS = ["/common/home/rbk70/projects/DataMake/providers/board/arrows1"]
COLORS = [
    (("#ffffff","#333333"),("#E18B47","#F18B47")),
]

pgn = open(PGN_LOCATION)

def randomArrowCordinates():

    def withinBoard(cord):
        if cord[0] < 0 or cord[0] > 7:
            return False
        elif cord[1] < 0 or cord[1] > 7:
            return False
        return True

    def randCord():
        return (randrange(0,8), randrange(0,8))
    
    def addCords(cords1,cords2):
        return (cords1[0] + cords2[0], cords1[1] + cords2[1])

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
        arrow_type = randrange(0,2)
        
        if arrow_type == 0:
            offset = choice(KNIGHTS)
            while True:
                cord = randCord() 
                target = addCords(cord,offset)
                if withinBoard(target):
                    break
            arrows.append((cord,target))
        elif arrow_type == 1:
            cord = randCord()
            while True:
                length = randrange(0,8)
                direction = randrange(0,8)
                if direction == 0:
                    offset = (0,length)
                elif direction == 1:
                    offset = (length,length)
                elif direction == 2:
                    offset = (length, 0)
                elif direction == 3:
                    offset = (length,-length)
                elif direction == 4:
                    offset = (0,-length)
                elif direction == 5:
                    offset = (-length,-length)
                elif direction == 6:
                    offset = (-length, 0)
                elif direction == 7:
                    offset = (-length, length)
                target = addCords(cord,offset)
                if withinBoard(target):
                    break
            arrows.append((cord,target))
    return arrows

def create():
    size = randrange(200, 800)
    theme = choice(COLORS)
    
    game = chess.pgn.read_game(pgn)
    board = game.board()
    moves = list(game.mainline_moves())
    target_move = randrange(0,len(moves))
    for x in range(target_move):
        board.push(moves[x])
    arrows = fenToImage(
        fen=board.fen(),
        squarelength=int(size / 8),
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
        Arrows=randomArrowCordinates(),
    )
    return {"image": arrows, "annotations": None}
