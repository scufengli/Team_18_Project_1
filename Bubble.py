import pygame, os
from Settings import *
from Entity import Entity

class Bubble(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y, 18)

        self.counter = 0
        self.movement = 1
        self.center()

        self.sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'bubble.mp3'))

    def float(self):
      if self.counter % 20 == 0:
         self.movement *= -1

      self.rect.y += self.movement
      self.counter += 1

    def update(self, display_surf):
      self.float()
      super().update(display_surf)