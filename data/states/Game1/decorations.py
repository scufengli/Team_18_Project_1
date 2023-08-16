import pygame as pg
from ... import prepare as mp
from ... import tools as mt 
from random import randint, choice
from .tilesV2 import *

class Sky:
    def __init__(self,horizon):
        self.horizon = horizon 
        self.top = pg.image.load('resources/graphics/level_graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pg.image.load('resources/graphics/level_graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pg.image.load('resources/graphics/level_graphics/decoration/sky/sky_middle.png').convert()
        
        # STRETCH
        self.top = pg.transform.scale(self.top,(mp.screen_width,mp.tile_size))
        self.bottom = pg.transform.scale(self.bottom,(mp.screen_width,mp.tile_size))
        self.middle = pg.transform.scale(self.middle,(mp.screen_width,mp.tile_size))

    def draw(self,surface):
        for row in range(mp.vertical_tile_number):
            y = row * mp.tile_size
            if row < self.horizon:
                surface.blit(self.top,(0,y))
            elif row == self.horizon:
                surface.blit(self.middle,(0,y))
            else:
                surface.blit(self.bottom,(0,y))

class Water:
    def __init__(self,top,level_width):
        water_start = -mp.screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + mp.screen_width) / water_tile_width)
        self.water_sprites = pg.sprite.Group()

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
        cloud_surf_list = mt.import_folder('resources/graphics/level_graphics/decoration/clouds')
        min_x = -mp.screen_width
        max_x = level_width + mp.screen_width
        min_y = 0 
        max_y = horizon
        self.cloud_sprites = pg.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x,max_x)
            y = randint(min_y,max_y)
            sprite = StaticTile(0,x,y,cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface,shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
