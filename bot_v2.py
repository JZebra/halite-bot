import logging
import pdb

from hlt import *
from node import MapNode
from tree import MapTree

logging.basicConfig(filename='bot.log', level=logging.DEBUG)
_log = logging.getLogger(__name__)


class TargetingError(Exception):
    def __init__(self, message):
        self.message = message


class TreeError(Exception):
    def __init__(self, message):
        self.message = message


class JZBot:

    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.neutral_id = 0
        self.str_cap = 255

    def store_map(self, game_map):
        self.game_map = game_map
        self.tree = self.gen_quadtree(game_map)

    def generate_moves(self, game_map):
        """Public interface with bot runner
        """
        self.store_map(game_map)
        moves = []
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                location = Location(x, y)
                site = self.game_map.getSite(location)
                if site.is_friend():
                    moves.append(self.move(location))
        return moves

    def move(self, location):
        src = self.game_map.getSite(location)

        # capture if possible
        capture_move = self.capture(src)
        if capture_move:
            return capture_move

        # farm if needed
        if self.should_farm(src):
            return Move(src, STILL)

        return self.march(src)

    def can_capture(self, src, dest):
        return src.strength > dest.strength

    def capture_score(self, site):
        """Site production is not correlated with strength
        """
        # default value
        site_strength = site.strength or 1
        return float(site.production) / float(site_strength)

    def can_be_countered(self, src, dest):
        """Returns true if a capturing move can be countered
        """
        next_str = src.strength - dest.strength
        for direction in CARDINALS:
            neighbor = self.game_map.getSite(src, direction)
            if neighbor.is_enemy():
                enemy_next_str = neighbor.strength + neighbor.production
                if next_str < enemy_next_str:
                    return True
        return False

    def capture(self, site):
        best_score = -1
        capture_dir = None
        friend_count = 0

        for direction in CARDINALS:
            neighbor = self.game_map.getSite(site, direction)
            if neighbor.is_friend():
                friend_count += 1
            else:
                if self.can_capture(site, neighbor) and not\
                        self.can_be_countered(site, neighbor):
                    score = self.capture_score(neighbor)
                    if score > best_score:
                        best_score = score
                        capture_dir = direction

        # deprioritize expanding in favor of marching
        if friend_count > 2:
            return None
        elif capture_dir:
            return Move(site, capture_dir)
        else:
            return None

    def should_farm(self, location):
        site = self.game_map.getSite(location)
        return site.strength < site.production * 5

    def march(self, src):
        """Determines a direction to move
        Params
        src - Site object

        Returns
        move - Move object
        """
        target = self.find_nearest_target(src)
        if not target:
            direction = STILL
        else:
            direction = self.find_direction(src, target)
            # don't commit suicide
            dest = self.game_map.getSite(src, direction)
            if not dest.is_friend() and not self.can_capture(src, dest):
                direction = STILL
        return Move(src, direction)

    def find_nearest_target(self, loc):
        """Traverses the quadtree to find the nearest enemy or neutral site.
        Returns False if loc is already adjacent to an enemy or neutral site
        """
        src = self.game_map.getSite(loc)
        node = self.tree.find_node(src)
        if not node:
            raise TreeError("could not find a node with {0}".format(src))

        # default to large number
        best_distance = 255
        target = None

        # move up a level to look for targets
        for dest in node.parent.sites:
            if dest.is_enemy():
                distance = self.game_map.getDistance(src, dest)
                if distance < best_distance:
                    best_distance = distance
                    target = dest
        if not target:
            raise TargetingError("find_nearest_target did not find a target")

        if best_distance == 1:
            return False
        else:
            return target

    def find_direction(self, src, dest):
        """Params can be Locations or Sites
        """
        angle = self.game_map.get_angle(src, dest)
        if (-1/4 * math.pi) <= angle < (1/4 * math.pi):
            return EAST
        elif (1/4 * math.pi) <= angle < (3/4 * math.pi):
            # this would normally be north, but y = 0 is at the top of the map
            # and y = map height is at the bottom
            return SOUTH
        elif (3/4 * math.pi) <= angle or angle < (-3/4 * math.pi):
            return WEST
        elif (-3/4 * math.pi) <= angle < (-1/4 * math.pi):
            return NORTH

    def gen_quadtree(self, game_map):
        rect = (0, 0, game_map.width, game_map.height)
        root = MapNode(None, rect, self.game_map)
        tree = MapTree(root, 1)
        return tree
