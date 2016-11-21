import logging
import math

from hlt import *
from networking import *

logging.basicConfig(filename='middleOut01.log',level=logging.DEBUG)

myID, gameMap = getInit()
STR_CAP = 255
sendInit("middle_out_01")


def move(location, border_map):
    site = gameMap.getSite(location)

    # capture neighbor if possible
    capture_move = capture(location)
    if capture_move:
        logging.info('capturing move')
        return capture_move

    # farm if needed
    if should_farm(location):
        logging.info('farming move')
        return Move(location, STILL)

    # move outwards towards nearest border
    logging.info('marching')
    return should_march(location, border_map)

def can_capture(src_site, dest_site):
    if src_site.strength > dest_site.strength:
        return True
    return False

def capture(location):
    site = gameMap.getSite(location)
    for direction in CARDINALS: 
        neighbor = gameMap.getSite(location, direction)
        is_friendly = neighbor.owner == site.owner
        if can_capture(site, neighbor) and not is_friendly:
            return Move(location, direction)
    return None


def should_farm(location):
    site = gameMap.getSite(location)
    return site.strength < site.production * 5


def should_march(location, border_map):
    site = gameMap.getSite(location)
    best_distance = 30
    target_location = None

    for border_location in border_map:
        distance = gameMap.getDistance(location, border_location)
        if distance < best_distance:
            best_distance = distance
            target_location = border_location

    # Don't move if we can't capture the target
    target_site = gameMap.getSite(target_location)
    if not can_capture(site, target_site):
        return Move(location, STILL)

    diff_x = location.x - target_location.x
    diff_y = location.y - target_location.y
    if abs(diff_x) > abs(diff_y):
        if diff_y > 0:
            direction = EAST
        else:
            direction = WEST
    else:
        if diff_x > 0:
            direction = SOUTH
        else:
            direction = NORTH

    return Move(location, direction)


def is_boundary(location):
    site = gameMap.getSite(location)
    if site.owner == myID:
        return False

    for direction in CARDINALS:
        neighbor = gameMap.getSite(location, direction)
        if neighbor.owner == site.owner:
            return True
    return False


def generate_borders(gameMap):
    boundary_tiles = []
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if is_boundary(location):
                boundary_tiles.append(location)

    return boundary_tiles


while True:
    moves = []
    gameMap = getFrame()

    border_map = generate_borders(gameMap)

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location, border_map))

    sendFrame(moves)

