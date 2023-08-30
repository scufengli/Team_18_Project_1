import pygame, os
from .Settings import *
from .Entity import Entity

class Spear(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y, 24)
               
        self.counter = 0
        self.movement = 1
        self.center()

        self.pickup_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'spear_pickup.mp3'))

    def float(self):
        if self.counter % 15 == 0:
            self.movement *= -1

        self.rect.y += self.movement

    def update(self, display_surf):
        self.counter += 1
        if self.counter % 5 == 0:
            self.float()
        super().update(display_surf)