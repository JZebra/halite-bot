import logging
import pdb

from action import Action
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
        self.last_actions = []

        # territory edges
        self.rightmost_x = 0
        self.bottommost_y = 255
        self.topmost_y = 0
        self.distances = {}

    def generate_moves(self, game_map):
        """Public interface with bot runner
        """
        moves = []
        self.game_map = game_map
        pdb.set_trace()

        self.tree = self.gen_quadtree(game_map)

        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                location = Location(x, y)
                site = self.game_map.getSite(location)
                if site.is_friend():
                    moves.append(self.move(location))
        return moves

    def move(self, location):
        # capture if possible
        capture_move = self.capture(location)
        if capture_move:
            return capture_move

        # farm if needed
        if self.should_farm(location):
            return Move(location, STILL)

        return self.march(location)

    def can_capture(self, src_site, dest_site):
        if src_site.owner != dest_site.owner and\
                src_site.strength > dest_site.strength:
            return True
        return False

    def capture_score(self, site):
        """Site production is not correlated with strength
        """
        # default value
        site_strength = site.strength or 1
        return float(site.production) / float(site_strength)

    def can_be_countered(self, src_loc, dest_loc):
        """Returns true if a capturing move can be countered
        """
        src_site = self.game_map.getSite(src_loc)
        dest_site = self.game_map.getSite(dest_loc)
        next_str = src_site.strength - dest_site.strength
        for direction in CARDINALS:
            neighbor = self.game_map.getSite(src_loc, direction)
            if neighbor.is_enemy():
                enemy_next_str = neighbor.strength + neighbor.production
                if next_str < enemy_next_str:
                    return True
        return False

    def capture(self, location):
        best_score = -1
        capture_dir = None
        site = self.game_map.getSite(location)

        for direction in CARDINALS:
            neighbor = self.game_map.getLocation(location, direction)
            neighbor_site = self.game_map.getSite(location, direction)
            if self.can_capture(site, neighbor_site) and not\
                    self.can_be_countered(location, neighbor):
                score = self.capture_score(neighbor_site)
                if score > best_score:
                    best_score = score
                    capture_dir = direction

        if capture_dir:
            return Move(location, capture_dir)
        else:
            return None

    def should_farm(self, location):
        site = self.game_map.getSite(location)
        return site.strength < site.production * 5

    def march(self, src):
        """Determines a direction to move
        Params
        src - Location object

        Returns
        move - Move object
        """
        target = self.find_nearest_target(src)
        _log.info("target is {0}".format(repr(target)))
        if not target:
            direction = STILL
        else:
            direction = self.find_direction(src, target)

        _log.info("direction is {0}".format(direction))

        # continue moving in the same direction if we marched before
        # for action in self.last_actions:
        #     if action.has_end(src):
        #         direction = action.direction
        #         self.last_actions.remove(action)
        #         break

        # # add to last_actions
        # if not direction:
        #     direction = self.direction_to_border(src)

        # dest = self.game_map.getLocation(src, direction)
        # action = Action(src, dest, direction)
        # self.store_action(action)

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
            if not dest.is_friend():
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
        dx = dest.x - src.x
        dy = dest.y - src.y
        if abs(dx) > abs(dy):
            if dx > 0:
                return EAST
            else:
                return WEST
        else:
            if dy > 0:
                return SOUTH
            else:
                return NORTH

    def is_stored_destination(self, location):
        return any(action.has_end(location) for action in self.last_actions)

    def store_action(self, action):
        """Returns False and does not store the action if the destination exists
        in an existing action
        """
        if self.is_stored_destination(action.end):
            return False
        else:
            self.last_actions.append(action)
            return True

    def gen_quadtree(self, game_map):
        rect = 0, 0, game_map.width, game_map.height
        root = MapNode(None, rect, self.game_map)
        tree = MapTree(root, 1)
        return tree
