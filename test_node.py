import unittest

from hlt import GameMap
from node import MapNode


class MapNodeTest(unittest.TestCase):

    def create_sample_map(self):
        # init map
        game_map = GameMap(width=3, height=3, num_players=2, bot_id=1)
        # iterate and set neutral squares
        for y in range(game_map.height):
            for x in range(game_map.width):
                game_map.contents[y][x].owner = 0

        # create non-neutral squares
        game_map.contents[0][0].owner = 1
        game_map.contents[1][1].owner = 2
        return game_map

    def create_sample_node(self):
        m = self.create_sample_map()
        return MapNode(None, (0, 0, m.width, m.height), m)

    def setUp(self):
        self.node = self.create_sample_node()

    def test_contains_enemy(self):
        self.assertTrue(self.node.contains_enemy())
        for site in self.node.sites:
            site.owner = 1
        self.assertFalse(self.node.contains_enemy())

    def test_contains_friend(self):
        self.assertTrue(self.node.contains_friend())
        for site in self.node.sites:
            site.owner = 2
        self.assertFalse(self.node.contains_friend())

    def test_spans_feature(self):
        rect = (0, 0, self.node.game_map.width, self.node.game_map.height)
        self.assertTrue(self.node.spans_feature(rect))
        for site in self.node.sites:
            site.owner = 2
        self.assertFalse(self.node.spans_feature(rect))

    def test_has_children(self):
        self.assertFalse(self.node.has_children())
        self.node.subdivide()
        self.assertTrue(self.node.has_children())


if __name__ == '__main__':
    unittest.main()
