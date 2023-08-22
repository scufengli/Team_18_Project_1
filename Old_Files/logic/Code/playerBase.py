import pygame
from support import import_folder

class PlayerBase(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {'Idle': []}
        self.frame_index = 0
        self.import_character_assets()

        self.image = self.animations['Idle'][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        self.speed = 8
        self.direction = pygame.math.Vector2(0,0)

        self.on_left = False
        self.on_right = False


    def import_character_assets(self):
        character_path = '../Graphics/Character/'

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)