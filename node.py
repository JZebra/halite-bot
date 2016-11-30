from quadtree import Node


class MapNode:
    """Extends the quadtree node class to handle the bot game_map
    """

    def __init__(self, parent, rect, game_map):
        super(parent, rect)
        x0, x1, y0, y1 = rect
        sites = []
        for y in range(y0, y1):
            for x in range(x0, x1):
                sites.append(game_map.contents[y][x])
        self.sites = sites

    def getinstance(self, rect):
        return MapNode(self, rect)

    def spans_feature(self, rect):
        return self.contains_enemy(self.sites)

    def contains_enemy(self, sites):
        return any(site.is_enemy() for site in sites)

    # def is_enemy_site(self, site):
    #     return site.owner != self.bot_id
