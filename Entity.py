from Settings import *
import pygame

class Entity:
    def __init__(self, x = 0, y = 0, size = 70):
        self.size = size
        self.rect = pygame.Rect(x, y, self.size, self.size)

        self.frames = None
        self.animations = {'idle': None}
        self.state = 'idle'

    def animation_setup(self, animations):
        for state in self.animations.keys():
            self.animations[state] = animations[state]

        self.frames = self.animations[self.state]

    def update(self, display_surf):
        self.frames = self.animations[self.state]
        pygame.draw.rect(display_surf, rect = self.rect, color = (255, 0, 0))
        display_surf.blit(self.frames.next(), (self.rect.x, self.rect.y))

    def collide_rect(self, entity):
        collided = self.rect.scale_by(COLLISION_FACTOR). \
            colliderect(entity.rect.scale_by(COLLISION_FACTOR))
        return collided
    