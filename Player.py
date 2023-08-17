from Settings import *
from Character import Character
from SpriteStripAnim import SpriteStripAnim

class Player(Character):
    def __init__(self, animations):
        super().__init__(animations)
        self.speed = 2
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE

    def is_escaped(self, escape_point):
        return self.x + PLAYER_SIZE / 2 > escape_point.get_x_lower() and \
         self.x + PLAYER_SIZE / 2 < escape_point.get_x_upper() and \
          self.y + PLAYER_SIZE / 2 > escape_point.get_y_lower() and \
           self.y + PLAYER_SIZE / 2 < escape_point.get_y_upper()