import logging

from hlt import *
from networking import *

_log = logging.getLogger(__name__)

myID, gameMap = getInit()
sendInit("middle_out_00")


def move(location):
    site = gameMap.getSite(location)
    if site.strength < site.production * 5:
        return Move(location, STILL)
    return Move(location, int((random.random() * 4) + 1))


while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))

    sendFrame(moves)
