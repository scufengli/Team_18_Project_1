import pygame
from Settings import *
from Character import Character
from SpriteStripAnim import SpriteStripAnim

class Player(Character):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)

        self.lives_offset = 0   
        self.freeze = False
        self.counter = 0
        self.armed = False

    def is_player(self):
        return True
    
    def update(self, display_surf):
        if self.freeze is True:
            self.frames.blink()
        else:
            self.frames.unblink()

        super().update(display_surf)