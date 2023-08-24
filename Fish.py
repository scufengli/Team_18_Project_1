import pygame, os
from Settings import *
from Character import Character

class Fish(Character):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y, 24)

        self.counter = 0
        self.x_movement = 1
        self.state = 'move_right'

        self.death_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'fish_death.mp3'))

    def patrol(self):
        if self.counter % 15 == 0:
            self.x_movement *= -1
        
        if self.counter % 120 == 0:
            self.speed *= -1
            if self.state == 'move_left':
                self.state = 'move_right'
            else:
                self.state = 'move_left'

        self.rect.y += self.x_movement
        self.rect.x += self.speed
        self.counter += 1

    def update(self, display_surf):
        self.patrol()
        super().update(display_surf)