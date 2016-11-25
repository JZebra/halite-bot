import logging
import pdb

from action import Action
from hlt import *
from networking import *
# from socket_networking import *


class MiddleOutBot:

    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.neutral_id = 0
        self.str_cap = 255
        self.last_actions = []

    def generate_moves(self, game_map):
        """Public interface with bot runner
        """
        moves = []
        self.game_map = game_map
        self.border_map = self.generate_borders(game_map)

        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                location = Location(x, y)
                if self.game_map.getSite(location).owner == self.bot_id:
                    moves.append(self.move(location))
        return moves

    def move(self, location):
        # capture neighbor if possible
        capture_move = self.capture(location)
        if capture_move:
            return capture_move

        # farm if needed
        if self.should_farm(location):
            return Move(location, STILL)

        # move outwards towards nearest border
        return self.march(location)

    def is_enemy(self, site):
        return site.owner != self.bot_id and site.owner != self.neutral_id

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
            if self.is_enemy(neighbor):
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
        # initialize to largest map
        direction = None

        # continue moving in the same direction if we marched before
        for action in self.last_actions:
            if action.has_end(src):
                direction = action.direction
                self.last_actions.remove(action)
                break

        # add to last_actions
        if not direction:
            direction = self.direction_to_border(src)

        dest = self.game_map.getLocation(src, direction)
        action = Action(src, dest, direction)
        self.store_action(action)
        return Move(src, direction)

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

    def direction_to_border(self, location):
        """Returns a direction. Returns STILL if location is adjacent to border
        """
        best_distance = 255
        for border_location in self.border_map:
            distance = self.game_map.getDistance(location, border_location)
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
        return STILL

    def is_boundary(self, location):
        site = self.game_map.getSite(location)
        if site.owner == self.bot_id:
            return False

        for direction in CARDINALS:
            neighbor = self.game_map.getSite(location, direction)
            if neighbor.owner == site.owner:
                return True
        return False

    def generate_borders(self, game_map):
        """Returns a list of the outer boundary tiles
        """
        boundary_tiles = []
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                location = Location(x, y)
                if self.is_boundary(location):
                    boundary_tiles.append(location)

        return boundary_tiles
