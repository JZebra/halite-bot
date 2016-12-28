from hlt import *
import socket
import traceback
import struct
from ctypes import *
import sys

_productions = []
_width = -1
_height = -1
_connection = None

def serializeMoveSet(moves):
    returnString = ""
    for move in moves:
        returnString += str(move.loc.x) + " " + str(move.loc.y) + " " + str(move.direction) + " "
    return returnString

def deserializeMapSize(inputString):
    splitString = inputString.split(" ")

    global _width, _height
    _width = int(splitString.pop(0))
    _height = int(splitString.pop(0))

def deserializeProductions(inputString):
    splitString = inputString.split(" ")

    for a in range(0, _height):
        row = []
        for b in range(0, _width):
            row.append(int(splitString.pop(0)))
        _productions.append(row)

def deserializeMap(inputString, bot_id):
    splitString = inputString.split(" ")

    m = GameMap(_width, _height, bot_id=bot_id)

    y = 0
    x = 0
    counter = 0
    owner = 0
    while y != m.height:
        counter = int(splitString.pop(0))
        owner = int(splitString.pop(0))
        for a in range(0, counter):
            m.contents[y][x].owner = owner
            x += 1
            if x == m.width:
                x = 0
                y += 1

    for a in range(0, _height):
        for b in range(0, _width):
            m.contents[a][b].strength = int(splitString.pop(0))
            m.contents[a][b].production = _productions[a][b]

    return m

def sendString(toBeSent):
    global _connection
    toBeSent += '\n'
    _connection.sendall(bytes(toBeSent, 'ascii'))

def getString():
    global _connection
    newString = ""
    buffer = '\0'
    while True:
        buffer = _connection.recv(1).decode('ascii')
        if buffer != '\n':
            newString += str(buffer)
        else:
            return newString

def getInit():
    # Connect to environment.
    global _connection
    _connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # port = int(input('Enter the port on which to connect: '))
    port = int(3000)
    _connection.connect(('localhost', port))
    print('Connected to intermediary on port #' + str(port))
    bot_id = get_player_id()
    m = get_map(bot_id)

    return (bot_id, m)

def get_player_id():
    playerTag = int(getString())
    return playerTag

def get_map(bot_id):
    deserializeMapSize(getString())
    deserializeProductions(getString())
    m = deserializeMap(getString(), bot_id)
    return m

def sendInit(name):
    sendString(name)

def getFrame(bot_id):
    return deserializeMap(getString(), bot_id)

def sendFrame(moves):
    sendString(serializeMoveSet(moves))
