import logging

from quadtree import QuadTree

logging.basicConfig(filename='bot.log', level=logging.DEBUG)
_log = logging.getLogger(__name__)


class MapTree(QuadTree):

    def __init__(self, rootnode, minrect):
        super().__init__(rootnode, minrect)

    def find_node(self, site, starting_node=None):
        """finds the deepest node that includes the site. Defaults to the root
        """
        # default to root
        # _log.info('===========')
        result = False
        if starting_node is None:
            starting_node = self.allnodes[0]
            # _log.info('defaulting to root node with rect {0}'.format(starting_node.rect))

        # base case: return node if it's a leaf node
        # _log.info(starting_node.has_children())
        # _log.info(site in starting_node.sites)
        if not starting_node.has_children() and site in starting_node.sites:
            # _log.info('base case')
            return starting_node

        # recursion
        # _log.info('going through children of {0}'.format(starting_node))
        for child in starting_node.children:
            if child is not None:
                result = self.find_node(site, child)
                if result:
                    return result
