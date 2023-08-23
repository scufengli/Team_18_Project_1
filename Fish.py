from Settings import *
from Character import Character

class Fish(Character):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)

    def update(self, display_surf):
      display_surf.blit(self.frames.next(), (self.rect.x + BLOCK_SIZE / 2, self.rect.y + BLOCK_SIZE / 2))