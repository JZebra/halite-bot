class Action:

    def __init__(self, loc1, loc2, direction):
        self.start = loc1
        self.end = loc2
        self.direction = direction

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.start.__dict__ == other.start.__dict__ and\
                self.end.__dict__ == other.end.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class):
            return not self.__eq__(other)
        return NotImplemented

    def has_same_end(self, location):
        """Use this to compare two Locations because Locations that
        have the same coordinates can still be different objects
        """
        return self.end.__dict__ == location.__dict__

    # because we don't override __hash__(), sets will not function as expected
    # def __hash__(self):
    #     return hash(tuple(sorted(self.__dict__.items())))
