from .Settings import *
import pygame

class Entity:
    def __init__(self, x = 0, y = 0, size = BLOCK_SIZE):
        self.size = size
        self.rect = pygame.Rect(x, y, self.size, self.size)

        self.frames = None
        self.animations = {'idle': None}
        self.state = 'idle'

    def center(self):
        self.rect.x += BLOCK_SIZE / 2 - self.size / 2
        self.rect.y += BLOCK_SIZE / 2 - self.size / 2

    def animation_setup(self, animations):
        for state in self.animations.keys():
            self.animations[state] = animations[state]

        self.frames = self.animations[self.state]

    def update(self, display_surf):
        self.frames = self.animations[self.state]
        display_surf.blit(self.frames.next(), (self.rect.x, self.rect.y))

    def collide_rect(self, entity):
        collided = self.rect.scale_by(COLLISION_FACTOR). \
            colliderect(entity.rect.scale_by(COLLISION_FACTOR))
        return collided
    
    def is_player(self):
        return False
    