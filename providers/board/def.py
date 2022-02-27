import json
from fentoboardimage import fenToImage, loadPiecesFolder, loadArrows
import random
from random import randint, choice, randrange
import chess.pgn

PGN_LOCATION = "/home/reed/Github/DataMake/providers/board/lichess_db_standard_rated_2013-01.pgn"
SETS = [
        "/home/reed/Github/DataMake/providers/board/pieces",
        "/home/reed/Github/DataMake/providers/board/pieces2",
        "/home/reed/Github/DataMake/providers/board/pieces3",
        "/home/reed/Github/DataMake/providers/board/pieces4",
       ]
ARROW_SETS = [
        "/home/reed/Github/DataMake/providers/board/arrows1",
        "/home/reed/Github/DataMake/providers/board/arrows2",
    ]
COLORS = [
    (("#eeeed2","#769656"),("#eeeed2","#baca2b")),
    (("#656260","#312e2b"),("#397e97","#1f647d")),
    (("#f0d8bf","#ba5546"),("#f4e8a9","#d9a76c")),
    (("#f0d9b5","#b58863"),("#cdd26a","#aaa23a")),
    (("#dee3e6","#8ca2ad"),("#c3d887","#92b166")),
    (("#f1f6b2","#59935d"),("#8ed1bb","#349689"))
]

classes = ["BOARD","p","r","n","b","q","k","P","R","N","B","Q","K"]

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
                length = randrange(1,8)
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
    flipped = choice([True, False])
    size = randrange(400, 800)
    theme = choice(COLORS)
    square_length = int(size / 8)
    game = chess.pgn.read_game(pgn)
    board = game.board()
    moves = list(game.mainline_moves())
    min_move = 0
    if len(moves) > 10:
        min_move = 10
    target_move = randrange(min_move,len(moves))
    for x in range(target_move):
        board.push(moves[x])
    annotations = []
    annotations.append([0,size/2,size/2,size,size])
    for key, value in board.piece_map().items():
        if not flipped:
            key = 63 - key
        x = key % 8
        if not flipped:
            x = 7 - x
        y = int(key / 8)
        sym = value.symbol()
        class_index = classes.index(sym)
        annotations.append([class_index,x*square_length + 1/2 * square_length,y*square_length + 1/2 * square_length,square_length * 0.8,square_length * 0.8])       
    arrows = fenToImage(
        fen=board.fen(),
        squarelength=square_length,
        pieceSet=loadPiecesFolder(choice(SETS)),
        darkColor=theme[0][1],
        lightColor=theme[0][0],
        flipped=flipped,
        lastMove={
            "before": (randrange(0,8), randrange(0,8)),
            "after": (randrange(0,8), randrange(0,8)),
            "darkColor": theme[1][1],
            "lightColor": theme[1][0],
        },
        ArrowSet=loadArrows(choice(ARROW_SETS)),
        Arrows=randomArrowCordinates(),
    )
    return {"image": arrows, "labels": annotations}
