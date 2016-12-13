from hlt import *
from bot_v2 import JZBot
# from networking import *
from socket_networking import *

my_id, game_map = getInit()
sendInit("jz_02")
bot = JZBot(my_id)

while True:
    moves = []
    game_map = getFrame(my_id)
    moves = bot.generate_moves(game_map)
    sendFrame(moves)
