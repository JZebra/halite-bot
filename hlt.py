import random
import math
import copy

STILL = 0
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4

DIRECTIONS = [a for a in range(0, 5)]
CARDINALS = [a for a in range(1, 5)]

ATTACK = 0
STOP_ATTACK = 1

NEUTRAL_ID = 0


class Location:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{0}, {1}".format(self.x, self.y)


class Site:
    def __init__(self, owner=0, strength=0, production=0, x=0, y=0, bot_id=None):
        self.owner = owner
        self.strength = strength
        self.production = production
        self.x = x
        self.y = y
        self.bot_id = bot_id

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "location: ({0}, {1}), owner: {2}, str: {3}".format(
            self.x, self.y, self.owner, self.strength)

    def is_friend(self):
        return self.owner == self.bot_id

    def is_neutral(self):
        return self.owner == NEUTRAL_ID

    def is_enemy(self):
        return not self.is_friend() and not self.is_neutral()


class Move:
    def __init__(self, loc=0, direction=0):
        self.loc = loc
        self.direction = direction


class GameMap:
    def __init__(self, width=0, height=0, num_players=0, bot_id=None):
        self.width = width
        self.height = height
        self.contents = []

        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                row.append(Site(0, 0, 0, x, y, bot_id))
            self.contents.append(row)

    def inBounds(self, l):
        return l.x >= 0 and l.x < self.width and l.y >= 0 and l.y < self.height

    def getDistance(self, l1, l2):
        dx = abs(l1.x - l2.x)
        dy = abs(l1.y - l2.y)
        if dx > self.width / 2:
            dx = self.width - dx
        if dy > self.height / 2:
            dy = self.height - dy
        return dx + dy

    def get_angle(self, l1, l2):
        dx = l2.x - l1.x
        dy = l2.y - l1.y

        if dx > self.width - dx:
            dx -= self.width
        elif -dx > self.width + dx:
            dx += self.width

        if dy > self.height - dy:
            dy -= self.height
        elif -dy > self.height + dy:
            dy += self.height
        return math.atan2(dy, dx)

    def getLocation(self, l, direction):
        if direction != STILL:
            l = copy.deepcopy(l)
            if direction == NORTH:
                if l.y == 0:
                    l.y = self.height - 1
                else:
                    l.y -= 1
            elif direction == EAST:
                if l.x == self.width - 1:
                    l.x = 0
                else:
                    l.x += 1
            elif direction == SOUTH:
                if l.y == self.height - 1:
                    l.y = 0
                else:
                    l.y += 1
            elif direction == WEST:
                if l.x == 0:
                    l.x = self.width - 1
                else:
                    l.x -= 1
        return l

    def getSite(self, l, direction = STILL):
        l = self.getLocation(l, direction)
        return self.contents[l.y][l.x]
