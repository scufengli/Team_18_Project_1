<<<<<<< HEAD:Player.py
import pygame, os
from Settings import *
from Character import Character

class Player(Character):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)
=======
from .Settings import*
from .Entity import*
from .SpriteStripAnim import*

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.speed = 25
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
>>>>>>> main:data/states/u_water_level/Player.py

        self.lives_offset = 0   
        self.freeze = False
        self.counter = 0
        self.armed = False
        self.hurt_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'player_hurt.mp3'))

    def is_player(self):
        return True
    
    def update(self, display_surf):
        super().update(display_surf)