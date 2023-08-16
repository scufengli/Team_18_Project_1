from Entity import Entity
from Settings import *

from SpriteStripAnim import SpriteStripAnim


class EscapePoint(Entity):
    def __init__(self, __x, __y):
        super().__init__()
        self.x = __x
        self.y = __y

        self.frames = SpriteStripAnim('Escape_Point.png', (0, 0, BLOCK_SIZE, BLOCK_SIZE), 5, -1, True, ANIMATION_FRAMES)

    def get_x_lower(self):
      return self.x

    def get_x_upper(self):
      return self.x + BLOCK_SIZE

    def get_y_lower(self):
      return self.y

    def get_y_upper(self):
      return self.y + BLOCK_SIZE

    def draw(self, displaySurface, escapeSurf):
      displaySurface.blit(escapeSurf, (self.x, self.y))