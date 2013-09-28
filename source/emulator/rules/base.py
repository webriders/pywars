__all__ = ['Action', 'Rule']


class Action(object):
    """
    Base class for defining action
    """
    duration = 0

    def __init__(self):
        self.tick = 0


class Rule(object):
    """
    Base class for defining rules
    Rule should implement resolve() method that should decide
    what to do with players on specified tick
    """
    def resolve(self, player, enemy):
        raise NotImplementedError()