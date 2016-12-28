from quadtree import Node


class MapNode(Node):
    """Extends the quadtree node class to handle the bot game_map
    """

    def __init__(self, parent, rect, game_map):
        super().__init__(parent, rect)
        self.game_map = game_map
        x0, y0, x1, y1 = rect
        sites = []
        for y in range(y0, y1):
            for x in range(x0, x1):
                sites.append(game_map.contents[y][x])
        self.sites = sites

    def getinstance(self, rect):
        return MapNode(self, rect, self.game_map)

    def spans_feature(self, rect):
        return self.contains_enemy() and self.contains_friend()

    def contains_enemy(self):
        return any(site.is_enemy() for site in self.sites)

    def contains_friend(self):
        return any(site.is_friend() for site in self.sites)

    def has_children(self):
        return any(child is not None for child in self.children)
