import logging
import math
import pdb

from action import Action
from hlt import *
from networking import *
# from socket_networking import *

logging.basicConfig(filename='middleOut02.log', level=logging.DEBUG)

my_id, game_map = getInit()
neutral_id = 0
STR_CAP = 255
last_actions = []
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
    return march(location, border_map)


def is_enemy(site):
    return site.owner != my_id and site.owner != neutral_id


def can_capture(src_site, dest_site):
    if src_site.owner != dest_site.owner and src_site.strength > dest_site.strength and not can_be_countered(src_site, dest_site):
        return True
    return False


def capture_score(site):
    """Site production is not correlated with strength
    """
    # default value
    site_strength = site.strength or 1
    return float(site.production) / float(site_strength)


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
    best_score = 0
    capture_dir = None

    for direction in CARDINALS:
        neighbor = game_map.getSite(location, direction)
        if can_capture(site, neighbor):
            score = capture_score(neighbor)
            if score > best_score:
                best_score = score
                capture_dir = direction

    if capture_dir:
        return Move(location, capture_dir)
    else:
        return None


def should_farm(location):
    site = game_map.getSite(location)
    return site.strength < site.production * 5


def march(location, border_map):
    site = game_map.getSite(location)
    # initialize to largest map
    target_location = None
    previous_dir = None
    global last_actions

    # continue moving in the same direction if we marched before
    # if any(action.has_same_end(location) for action in last_actions)


    # for action in last_actions:
    #     previous_dest = action[1]
    #     if previous_dest.x == location.x and previous_dest.y == location.y:
    #         previous_dir = action[2]
    #         last_actions.remove(action)

        # add to action log
    dir_to_border = direction_to_border(location, border_map)
    direction = previous_dir or dir_to_border or STILL
    dest_location = game_map.getLocation(location, direction)

    last_actions.append(tuple([location, dest_location, direction]))

    return Move(location, direction)


def is_stored_destination(location):
    return any(action.has_same_end(location) for action in last_actions)


def store_action(action):
    """Stores actions in a global variable.
    Returns False and does not store the action if the destination exists in
    an existing action
    """
    if is_stored_destination(action.end):
        return False
    else:
        global last_actions
        last_actions.append(action)
        return True



def direction_to_border(location, border_map):
    best_distance = 255
    for border_location in border_map:
        distance = game_map.getDistance(location, border_location)
        if distance < best_distance:
            best_distance = distance
            target_location = border_location

    # location is not at the border
    if best_distance >= 2:
        dx = location.x - target_location.x
        dy = location.y - target_location.y
        if abs(dx) > abs(dy):
            if dx > 0:
                direction = EAST
            else:
                direction = WEST
        else:
            if dy > 0:
                direction = SOUTH
            else:
                direction = NORTH
        return direction
    return None


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
    """Returns a list of the outer boundary tiles
    """
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

