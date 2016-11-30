from hlt import *
from bot_v1 import JZBot
from networking import *

# my_id, game_map = getInit()
my_id = get_player_id()
game_map = get_map(my_id)
sendInit("jz_01")
bot = JZBot(my_id)

while True:
    moves = []
    game_map = getFrame(my_id)
    moves = bot.generate_moves(game_map)
    sendFrame(moves)
