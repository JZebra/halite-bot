from hlt import GameMap
from node import MapNode


def create_sample_map():
    # init map
    game_map = GameMap(width=3, height=3, num_players=2, bot_id=1)
    # iterate and set neutral squares
    for y in range(game_map.height):
        for x in range(game_map.width):
            game_map.contents[y][x].owner = 0

    # create non-neutral squares
    game_map.contents[0][0].owner = 1
    game_map.contents[1][1].owner = 2
    return game_map


def create_sample_node():
    m = create_sample_map()
    return MapNode(None, (0, 0, m.width, m.height), m)
