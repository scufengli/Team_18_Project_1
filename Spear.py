import pygame, os
from Settings import *
from Entity import Entity

class Spear(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y, 24)
        self.center()

        self.pickup_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'spear_pickup.mp3'))
