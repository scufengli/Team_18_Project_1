from Settings import *
from Character import Character
from SpriteStripAnim import SpriteStripAnim

class Player(Character):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE

    def is_escaped(self, escape_point):
        return self.rect.x + PLAYER_SIZE / 2 > escape_point.get_x_lower() and \
         self.rect.x + PLAYER_SIZE / 2 < escape_point.get_x_upper() and \
          self.rect.y + PLAYER_SIZE / 2 > escape_point.get_y_lower() and \
           self.rect.y + PLAYER_SIZE / 2 < escape_point.get_y_upper()