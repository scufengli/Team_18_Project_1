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