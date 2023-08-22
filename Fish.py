from Entity import Entity
from Settings import *

from SpriteStripAnim import SpriteStripAnim

class Fish(Entity):
    def __init__(self, animations, __x, __y):
        super().__init__(animations)
        self.x = __x
        self.y = __y

    def update(self, display_surf):
      display_surf.blit(self.frames.next(), (self.x + BLOCK_SIZE / 2, self.y + BLOCK_SIZE / 2))