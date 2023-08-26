<<<<<<< HEAD:EscapePoint.py
from Settings import *
from Entity import Entity
=======
from .Entity import*
from .Settings import *

from .SpriteStripAnim import* 

>>>>>>> main:data/states/u_water_level/EscapePoint.py

class EscapePoint(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)