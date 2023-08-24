import pygame, os
from Settings import *

class HealthBar:
    def __init__(self):
        heart = pygame.image.load(os.path.join(ROOT_PATH, 'lives.png')).convert_alpha()
        heart.set_colorkey(heart.get_at((0, 0)), pygame.RLEACCEL)
        self.hrt_width, self.hrt_height = 24, 24
        self.heart = pygame.transform.scale(heart, (self.hrt_width, self.hrt_height)) # 330w x 197h

        life_bg = pygame.image.load(os.path.join(ROOT_PATH, 'lives_bg.png')).convert_alpha()
        life_bg.set_colorkey(life_bg.get_at((0, 0)), pygame.RLEACCEL)
        self.bg_width, self.bg_height = 249, 104
        self.life_bg = pygame.transform.scale(life_bg, (self.bg_width, self.bg_height)) # 249w x 104h

        self.display_x = 5
        self.display_y = 570

    def draw(self, lives_left, surface):
        life_rect = self.life_bg.get_rect()

        hrt_x = self.display_x + life_rect[0] + 50
        hrt_y = (life_rect[1] + (self.bg_height/2))-self.hrt_height/2 + 570
        #--^top of the bg_img + half of the bg_img height, - half of the heart height to get centered properly

        surface.blit(self.life_bg, (self.display_x, self.display_y))

        next = 0
        if lives_left > 0:
            for i in range(lives_left):
                surface.blit(self.heart, (hrt_x + next, hrt_y))
                next += 34
