import logging

from hlt import *
from middle_out_bot import MiddleOutBot
from networking import *
# from socket_networking import *

logging.basicConfig(filename='middleOut02.log', level=logging.DEBUG)

my_id, game_map = getInit()
sendInit("middle_out_02")
bot = MiddleOutBot(my_id)

while True:
    moves = []
    game_map = getFrame()
    moves = bot.generate_moves(game_map)
    sendFrame(moves)
