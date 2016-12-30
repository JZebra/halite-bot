import unittest

from hlt import Site
from test_helpers import create_sample_node
from tree import MapTree


class MapTreeTest(unittest.TestCase):

    def setUp(self):
        rootnode = create_sample_node()
        self.tree = MapTree(rootnode, 1)

    def test_find_node(self):
        target = Site(x=1, y=1)
        node = self.tree.find_node(target)
        self.assertIsNotNone(node)
        self.assertIn(target, node.sites)

        # all of a node's parents will have the site in node.sites.
        # make sure that this is the deepest node that contains the site
        for child in node.children:
            if child is not None:
                self.assertNotIn(target, child.sites)


if __name__ == '__main__':
    unittest.main()
