from hlt import *
from bot_v1 import JZBot
from networking import *

my_id, game_map = getInit()
sendInit("jz_01")
bot = JZBot(my_id)

while True:
    moves = []
    game_map = getFrame()
    moves = bot.generate_moves(game_map)
    sendFrame(moves)
