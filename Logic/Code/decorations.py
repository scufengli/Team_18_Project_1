import pygame
from settingsV2 import *

class Sky:
    def __init__(self,horizon):
        self.horizon = horizon
        self.top = pygame.image.load('../Logic/Graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('../Logic/Graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('../Logic/Graphics/decoration/sky/sky_middle.png').convert()

        # STRETCH
        self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
class Parallax_BG:
    def __init__(self):
        self.plx_imgs = []
        for i in range (1, 7):
            img = pygame.image.load(f"../Graphics/parallax_BG/forest_level_bg/forestBG_layer_{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(screen_width, screen_height))
            self.plx_imgs.append(img)


    def draw_bg(self, surface, scroll):
        for x in range(5):
            speed = 1
            for i in self.plx_imgs:
                surface.blit(i, ((x * screen_width)-scroll * speed,0))
                speed += 5
