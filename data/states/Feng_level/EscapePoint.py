from .Settings import *
from .Entity import Entity

class EscapePoint(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)