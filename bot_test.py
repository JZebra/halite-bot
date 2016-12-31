import unittest
from unittest.mock import Mock, patch

from hlt import *
from action import Action
from networking import getString, getInit

from bot_v2 import JZBot

class JZBotTest(unittest.TestCase):

    @patch('networking.getString')
    def init_bot_and_map(self, mock_getString):
        """getString() returns a series of ' ' delimited ints, the
        networking code builds the game map from these strings
        """
        bot_id = '1'
        map_size = '30 30'
        productions = '7 6 6 6 5 5 5 5 5 6 6 6 6 7 6 4 2 2 2 2 2 2 1 2 2 2 4 7 8 8 8 6 6 5 4 4 4 4 5 6 6 6 7 6 4 3 2 1 1 1 1 1 1 2 2 3 4 6 8 8 6 5 4 4 3 4 5 5 5 5 6 8 9 6 4 3 3 2 1 1 1 1 1 2 2 3 4 5 6 7 4 4 3 3 3 4 5 5 5 5 6 7 8 6 4 4 3 2 1 1 1 1 1 1 1 2 3 3 3 4 3 3 2 3 4 5 6 5 6 6 6 6 6 4 4 4 4 2 1 1 1 1 1 1 1 2 3 3 2 2 2 3 3 4 5 6 6 6 8 8 6 5 5 5 5 5 5 3 2 1 1 1 2 1 1 2 4 4 3 2 2 3 5 5 6 6 6 8 11 10 7 6 6 5 7 7 6 4 2 1 1 1 2 2 2 3 5 6 4 3 3 4 5 4 5 4 5 8 10 9 7 6 6 6 7 8 7 4 2 1 1 2 3 3 3 3 5 6 5 3 3 5 6 4 3 2 3 4 6 5 5 5 6 6 7 7 6 4 2 2 2 2 3 4 3 3 3 4 4 3 4 6 7 4 2 1 1 2 2 3 3 4 5 6 6 5 5 4 2 2 2 4 5 4 3 3 3 2 2 3 5 6 7 5 3 1 1 1 2 2 3 3 4 4 4 4 4 3 2 2 3 4 6 5 4 3 2 2 2 3 5 6 6 4 2 2 1 1 2 3 3 2 3 3 3 4 4 3 2 2 3 4 5 4 4 3 3 2 2 3 5 7 6 3 2 2 2 2 3 4 3 2 3 3 4 5 5 4 3 2 3 4 4 5 5 5 3 2 2 3 6 8 6 3 2 2 2 2 3 4 3 2 3 3 4 7 7 6 4 3 3 4 5 6 7 6 4 3 2 3 6 8 7 4 2 1 1 2 2 3 3 2 2 3 5 8 8 7 5 5 5 4 5 7 7 6 5 4 4 5 8 8 7 4 2 2 2 1 2 2 2 2 2 2 4 6 7 6 6 6 6 5 5 5 5 5 6 6 6 7 8 8 6 4 3 2 2 1 1 1 1 1 1 2 3 4 6 7 6 6 6 5 4 4 4 4 5 6 6 8 7 6 5 4 3 2 2 1 1 1 1 1 2 3 3 4 6 9 8 6 5 5 5 5 4 3 4 4 5 6 4 3 3 3 2 1 1 1 1 1 1 1 2 3 4 4 6 8 7 6 5 5 5 5 4 3 3 3 4 4 2 2 3 3 2 1 1 1 1 1 1 1 2 4 4 4 4 6 6 6 6 6 5 6 5 4 3 2 3 3 2 3 4 4 2 1 1 2 1 1 1 2 3 5 5 5 5 5 5 6 8 8 6 6 6 5 4 3 3 2 3 4 6 5 3 2 2 2 1 1 1 2 4 6 7 7 5 6 6 7 10 11 8 6 6 6 5 5 3 2 3 5 6 5 3 3 3 3 2 1 1 2 4 7 8 7 6 6 6 7 9 10 8 5 4 5 4 5 4 3 3 4 4 3 3 3 4 3 2 2 2 2 4 6 7 7 6 6 5 5 5 6 4 3 2 3 4 6 5 3 3 2 2 3 3 3 4 5 4 2 2 2 4 5 5 6 6 5 4 3 3 2 2 1 1 2 4 7 6 4 3 2 2 2 3 4 5 6 4 3 2 2 3 4 4 4 4 4 3 3 2 2 1 1 1 3 5 7 6 5 3 2 2 3 3 4 4 5 4 3 2 2 3 4 4 3 3 3 2 3 3 2 1 1 2 2 4 6 6 5 3 2 2 3 5 5 5 4 4 3 2 3 4 5 5 4 3 3 2 3 4 3 2 2 2 2 3 6 7 5 3 2 3 4 6 7 6 5 4 3 3 4 6 7 7 4 3 3 2 3 4 3 2 2 2 2 3 6 8 6 5 4 4 5 6 7 7 5 4 5 5 5 7 8 8 5 3 2 2 3 3 2 2 1 1 2 4 7 8 6'
        map_string = '22 0 1 2 434 0 1 1 442 0 78 65 51 44 34 26 24 23 29 41 38 28 18 18 35 64 83 102 66 35 33 39 51 67 62 44 37 53 74 76 74 71 64 52 35 24 21 23 36 55 52 37 21 19 34 55 56 56 34 22 27 36 43 54 49 38 32 40 58 66 66 70 73 58 36 27 26 28 42 64 58 44 27 21 29 38 35 31 22 18 25 35 38 46 46 45 42 45 53 59 58 63 69 55 37 33 36 35 43 59 56 43 26 17 21 25 21 17 14 15 24 36 38 46 53 61 60 59 59 56 64 58 51 38 29 31 40 37 36 47 53 44 26 16 20 28 20 13 11 15 25 37 42 60 83 89 70 60 64 67 77 54 35 26 25 28 36 36 31 36 44 37 23 17 27 42 30 18 13 16 25 36 54 91 136 142 92 63 70 87 80 50 29 22 26 28 32 38 32 35 39 29 21 22 33 50 41 30 23 27 37 52 88 131 168 168 110 74 81 99 67 43 29 23 30 36 45 62 48 42 40 32 35 43 41 48 43 40 34 38 52 76 125 164 179 172 122 85 84 90 41 36 33 26 33 49 74 102 76 55 44 43 64 80 57 37 27 27 24 27 36 50 79 97 97 92 65 46 46 50 31 33 30 25 35 53 81 105 74 51 41 49 81 100 73 35 17 15 16 19 26 30 38 40 37 35 25 19 20 26 37 37 30 28 41 56 74 81 57 40 39 49 77 90 75 38 16 12 14 20 29 31 29 24 21 21 16 14 17 26 37 36 29 31 42 54 66 67 53 43 49 60 77 71 58 31 14 12 13 16 26 29 25 19 19 20 15 14 17 26 35 39 35 39 49 60 64 61 50 49 67 93 112 76 44 22 12 11 11 15 24 29 24 18 17 18 15 15 17 25 40 48 43 43 55 72 71 60 48 51 76 126 162 103 49 22 13 14 14 18 26 32 29 24 21 21 19 20 24 31 60 68 53 40 47 65 66 52 41 43 58 107 150 101 57 27 16 17 20 26 30 29 28 29 28 31 32 34 44 55 76 74 53 37 44 62 67 51 39 33 35 66 102 83 64 35 18 18 28 38 41 29 23 24 26 34 44 51 65 78 66 58 40 32 38 49 54 43 36 27 22 34 56 56 55 34 19 21 37 52 55 36 23 21 24 35 52 64 71 74 59 53 45 42 45 46 46 38 35 25 18 22 31 35 38 29 21 27 44 58 64 42 28 26 27 36 58 73 70 66 56 59 59 60 61 53 46 38 36 24 15 14 17 21 25 21 17 26 43 56 59 43 35 36 33 37 55 69 63 58 67 64 60 70 89 83 60 42 37 25 15 11 13 20 28 20 16 26 44 53 47 36 37 40 31 29 38 51 58 64 87 70 63 92 142 136 91 54 36 25 16 13 18 30 42 27 17 23 37 44 36 31 36 36 28 25 26 35 54 77 99 81 74 110 168 168 131 88 52 37 27 23 30 41 50 33 22 21 29 39 35 32 38 32 28 26 22 29 50 80 90 84 85 122 172 179 164 125 76 52 38 34 40 43 48 41 43 35 32 40 42 48 62 45 36 30 23 29 43 67 50 46 46 65 92 97 97 79 50 36 27 24 27 27 37 57 80 64 43 44 55 76 102 74 49 33 26 33 36 41 26 20 19 25 35 37 40 38 30 26 19 16 15 17 35 73 100 81 49 41 51 74 105 81 53 35 25 30 33 31 26 17 14 16 21 21 24 29 31 29 20 14 12 16 38 75 90 77 49 39 40 57 81 74 56 41 28 30 37 37 26 17 14 15 20 19 19 25 29 26 16 13 12 14 31 58 71 77 60 49 43 53 67 66 54 42 31 29 36 37 25 17 15 15 18 17 18 24 29 24 15 11 11 12 22 44 76 112 93 67 49 50 61 64 60 49 39 35 39 35 31 24 20 19 21 21 24 29 32 26 18 14 14 13 22 49 103 162 126 76 51 48 60 71 72 55 43 43 48 40 55 44 34 32 31 28 29 28 29 30 26 20 17 16 27 57 101 150 107 58 43 41 52 66 65 47 40 53 68 60'
        mock_getString.side_effect = [bot_id, map_size, productions, map_string]
        # enemy site: location: (22, 0)
        # our site: location: (7, 15)

        bot_id, m = getInit()
        return bot_id, m

    def setUp(self):
        # init bot
        bot_id, m = self.init_bot_and_map()
        self.bot = JZBot(bot_id)
        self.bot.store_map(m)

        # make helper vars
        self.loc1 = Location(0, 0)
        self.loc2 = Location(0, 0)
        self.loc3 = Location(1, 1)
        # arbitrary
        self.direction = 1
        self.action1 = (Action(self.loc1, self.loc3, self.direction))
        self.action2 = (Action(self.loc2, self.loc3, self.direction))
        self.action3 = (Action(self.loc3, self.loc1, self.direction))
        self.action4 = (Action(self.loc3, self.loc2, self.direction))

    def test_find_direction_simple(self):
        loc1 = Location(2,2)
        loc2 = Location(2,4)
        loc3 = Location(4,2)
        loc4 = Location(4,5)

        self.assertEqual(self.bot.find_direction(loc1, loc2), SOUTH)
        self.assertEqual(self.bot.find_direction(loc2, loc1), NORTH)
        self.assertEqual(self.bot.find_direction(loc1, loc3), EAST)
        self.assertEqual(self.bot.find_direction(loc3, loc1), WEST)
        self.assertEqual(self.bot.find_direction(loc1, loc4), SOUTH)

    def test_find_direction_wrap(self):
        """ Not implemented yet
        """
        loc1 = Location(2,2)
        loc2 = Location(2,28)
        loc3 = Location(28,2)

        self.assertEqual(self.bot.find_direction(loc1, loc2), NORTH)
        self.assertEqual(self.bot.find_direction(loc2, loc1), SOUTH)
        self.assertEqual(self.bot.find_direction(loc1, loc3), WEST)
        self.assertEqual(self.bot.find_direction(loc3, loc1), EAST)

    def test_find_nearest_target(self):
        # m = self.bot.game_map
        starting_loc = Location(7, 15)
        target = self.bot.find_nearest_target(starting_loc)
        self.assertEqual(target.x, 22)
        self.assertEqual(target.y, 0)

    def test_march_no_target(self):
        starting_loc = Location(7, 15)
        src = self.bot.game_map.getSite(starting_loc)
        with patch.object(self.bot, 'find_nearest_target') as mock_fnt:
            # strong_dest = Site(x=0, y=0, strength=255)
            # weak_dest = Site(x=0, y=0, strength=10)
            mock_fnt.return_value = False
            self.assertEqual(self.bot.march(src).direction, STILL)

    def test_march_weak(self):
        starting_loc = Location(7, 15)
        src = self.bot.game_map.getSite(starting_loc)
        print(src)
        with patch.object(self.bot, 'find_nearest_target') as mock_fnt:
            # get the site at x=7, y=14. One square above our src
            dest = self.bot.game_map.contents[14][7]
            # make the destination weak
            dest.strength = 10
            mock_fnt.return_value = dest
            self.assertEqual(self.bot.march(src).direction, NORTH)

    def test_march_strong(self):
        starting_loc = Location(7, 15)
        src = self.bot.game_map.getSite(starting_loc)
        print(src)
        with patch.object(self.bot, 'find_nearest_target') as mock_fnt:
            # get the site at x=7, y=14. One square above our src
            dest = self.bot.game_map.contents[14][7]
            # make the destination strong
            dest.strength = 255
            mock_fnt.return_value = dest
            self.assertEqual(self.bot.march(src).direction, STILL)
