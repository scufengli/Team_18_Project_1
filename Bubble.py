from Entity import Entity
from Settings import *

from SpriteStripAnim import SpriteStripAnim

class Bubble(Entity):
    def __init__(self, animations, __x, __y):
        super().__init__(animations)
        self.x = __x
        self.y = __y
        self.counter = 0
        self.movement = 1

    def float(self):
      if self.counter % 15 == 0:
         self.movement *= -1

      self.y += self.movement
      self.counter += 1

    def update(self, display_surf):
      self.float()
      display_surf.blit(self.frames.next(), (self.x + BLOCK_SIZE / 2, self.y + BLOCK_SIZE / 2))