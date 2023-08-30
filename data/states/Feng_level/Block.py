from .Entity import Entity
from .Settings import *

class Block(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)