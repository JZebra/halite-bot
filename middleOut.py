import logging

from hlt import *
from networking import *

# logging.basicConfig(filename='middleOut.log',level=logging.DEBUG)

myID, gameMap = getInit()
STR_CAP = 255
sendInit("middle_out_00")


def move(location):
    site = gameMap.getSite(location)

    # capture neighbor if possible
    capture_move = capture(location)
    if capture_move:
        # logging.info('capturing move')
        return capture_move

    # farm if needed
    if should_farm(location):
        # logging.info('farming move')
        return Move(location, STILL)

    # if no enemies and above critical size, move to neighbor with highest piece value
    # logging.info('reinforcing move')

    return reinforce(location)

def capture(location):
    site = gameMap.getSite(location)
    has_enemies = False
    for direction in CARDINALS:
        neighbor = gameMap.getSite(location, direction)
        is_friendly = neighbor.owner == site.owner
        if neighbor.strength < site.strength and not is_friendly:
            return Move(location, direction)
    return None

def reinforce(location):
    site = gameMap.getSite(location)
    # default values
    strongest_neighbor = Site(strength=0)
    target_direction = None

    for direction in CARDINALS:
        neighbor = gameMap.getSite(location, direction)
        is_friendly = neighbor.owner == site.owner

        if neighbor.strength > strongest_neighbor.strength and is_friendly and neighbor.strength + strongest_neighbor.strength < STR_CAP:
            strongest_neighbor = neighbor
            target_direction = direction

    if target_direction:
        return Move(location, target_direction)
    else:
        return Move(location, STILL)


def should_farm(location):
    site = gameMap.getSite(location)
    return site.strength < site.production * 5


while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))

    sendFrame(moves)
