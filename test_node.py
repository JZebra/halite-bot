import unittest

from test_helpers import create_sample_node


class MapNodeTest(unittest.TestCase):

    def setUp(self):
        self.node = create_sample_node()

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
