from Entity import Entity
from Settings import *

from SpriteStripAnim import SpriteStripAnim

class Bubble(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)

        self.counter = 0
        self.movement = 1

    def float(self):
      if self.counter % 15 == 0:
         self.movement *= -1

      self.rect.y += self.movement
      self.counter += 1

    def update(self, display_surf):
      self.float()
      display_surf.blit(self.frames.next(), (self.rect.x + BLOCK_SIZE / 2, self.rect.y + BLOCK_SIZE / 2))