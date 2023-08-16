import pygame 
from random import randint, choice
from settingsV2 import *
from tilesV2 import *

class Sky:
    def __init__(self,horizon):
        self.horizon = horizon 
        self.top = pygame.image.load('../Graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('../Graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('../Graphics/decoration/sky/sky_middle.png').convert()
        
        # STRETCH
        self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
        self.bottom = pygame.transform.scale(self.bottom,(screen_width,tile_size))
        self.middle = pygame.transform.scale(self.middle,(screen_width,tile_size))

    def draw(self,surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top,(0,y))
            elif row == self.horizon:
                surface.blit(self.middle,(0,y))
            else:
                surface.blit(self.bottom,(0,y))

class Water:
    def __init__(self,top,level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top 
# =============== UNCOMMENT WHEN IMAGES ARE CREATED ==========================
            # sprite = AnimatedTile(192,X,Y,<WATER PATH>)
        #     self.water_sprites.add(sprite)

        # def draw(self,surface,shift):
        #     self.water_sprites.update(shift)
        #     self.water_sprites.draw(surface)
# =============== UNCOMMENT WHEN IMAGES ARE CREATED ==========================

class Clouds:
    def __init__(self,horizon,level_width,cloud_number):
        cloud_surf_list = import_folder('../Graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0 
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x,max_x)
            y = randint(min_y,max_y)
            sprite = StaticTile(0,x,y,cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface,shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
