import logging
import math
import pdb

from hlt import *
from networking import *
# from socket_networking import *

logging.basicConfig(filename='middleOut02.log',level=logging.DEBUG)

my_id, game_map = getInit()
neutral_id = 0
STR_CAP = 255
sendInit("middle_out_02")


def move(location, border_map):
    site = game_map.getSite(location)

    # capture neighbor if possible
    capture_move = capture(location)
    if capture_move:
        return capture_move

    # farm if needed
    if should_farm(location):
        return Move(location, STILL)

    # move outwards towards nearest border
    return should_march(location, border_map)


def is_enemy(site):
    return site.owner != my_id and site.owner != neutral_id


def can_capture(src_site, dest_site):
    if src_site.strength > dest_site.strength and not can_be_countered(src_site, dest_site):
        return True
    return False


def can_be_countered(src_site, dest_site):
    """Returns true if a capturing move can be countered
    """
    next_str = src_site.strength - dest_site.strength
    for direction in CARDINALS: 
        neighbor = game_map.getSite(location, direction)
        if is_enemy(neighbor):
            enemy_next_str = neighbor.strength + neighbor.production
            if next_str < enemy_next_str:
                return True
    return False


def capture(location):
    site = game_map.getSite(location)
    for direction in CARDINALS: 
        neighbor = game_map.getSite(location, direction)
        is_friendly = neighbor.owner == site.owner
        if can_capture(site, neighbor) and not is_friendly:
            return Move(location, direction)
    return None


def should_farm(location):
    site = game_map.getSite(location)
    return site.strength < site.production * 5


def should_march(location, border_map):
    site = game_map.getSite(location)
    # initialize to largest map
    best_distance = 255
    target_location = None

    for border_location in border_map:
        distance = game_map.getDistance(location, border_location)
        if distance < best_distance:
            best_distance = distance
            target_location = border_location

    # Don't move if we can't capture the target
    target_site = game_map.getSite(target_location)
    if best_distance >= 2: 
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
    else:
        return Move(location, STILL)



def is_boundary(location):
    site = game_map.getSite(location)
    if site.owner == my_id:
        return False

    for direction in CARDINALS:
        neighbor = game_map.getSite(location, direction)
        if neighbor.owner == site.owner:
            return True
    return False


def generate_borders(game_map):
    boundary_tiles = []
    for y in range(game_map.height):
        for x in range(game_map.width):
            location = Location(x, y)
            if is_boundary(location):
                boundary_tiles.append(location)

    return boundary_tiles


while True:
    moves = []
    game_map = getFrame()

    border_map = generate_borders(game_map)

    for y in range(game_map.height):
        for x in range(game_map.width):
            location = Location(x, y)
            if game_map.getSite(location).owner == my_id:
                moves.append(move(location, border_map))

    sendFrame(moves)

