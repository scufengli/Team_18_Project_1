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
        tile_x_amount = int((level_width + mp.screen_width) / water_tile_width) + 30
        self.water_sprites = pg.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192,x,y,'resources/graphics/level_graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self,surface,shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)


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

class CoinDisplay:
    def __init__(self):
        money_bag = pg.image.load('resources/graphics/background_assets/coin_bag.png').convert_alpha()
        self.mb_width,self.mb_height = 150,90
        self.money_bag = pg.transform.scale(money_bag, (self.mb_width, self.mb_height)) # 330w x 197h

        scroll_bg = pg.image.load('resources/graphics/background_assets/horz_scroll.png').convert_alpha()
        self.sc_width, self.sc_height = 260,66
        self.scroll_bg = pg.transform.scale(scroll_bg, (self.sc_width, self.sc_height)) # 230w x 210h

        self.display_x = 4
        self.display_y = 6
        self.txt_color = (0,0,0)

    def draw(self, coin_count, surface):
        font = pg.font.Font(mp.FONTS['Handjet-Regular'], 30)
        text_surface = font.render(coin_count, True, self.txt_color)
        text_rect = text_surface.get_rect()
        text_rect = self.scroll_bg.get_rect().center

        scroll_loc = self.money_bag.get_rect().center

        surface.blit(self.scroll_bg, (scroll_loc[0],int(scroll_loc[1])-23))
        surface.blit(self.money_bag, (self.display_x,self.display_y))
        surface.blit(text_surface, (text_rect[0]+(self.sc_width//4),text_rect[1]))

class LivesDisplay:
    def __init__(self):
        heart = pg.image.load('resources/graphics/background_assets/lives.png').convert_alpha()
        self.hrt_width, self.hrt_height = 24,24
        self.heart = pg.transform.scale(heart, (self.hrt_width, self.hrt_height)) # 330w x 197h

        life_bg = pg.image.load('resources/graphics/background_assets/lives_bg2.png').convert_alpha()
        self.bg_width, self.bg_height = 249,104
        self.life_bg = pg.transform.scale(life_bg, (self.bg_width, self.bg_height)) # 249w x 104h

        self.display_x = mp.SW_mid-(self.bg_width/2)
        self.display_y = 6

    def draw(self, lives_left, surface):
        life_rect = self.life_bg.get_rect()

        hrt_x = self.display_x + life_rect[0] + 50
        hrt_y = (life_rect[1] + (self.bg_height/2))-self.hrt_height/2 + 6
        #--^top of the bg_img + half of the bg_img height, - half of the heart height to get centered properly

        surface.blit(self.life_bg, (self.display_x, self.display_y))

        #next = 0
        if lives_left > 0:
            for i in range(lives_left):
                surface.blit(self.heart, (hrt_x, hrt_y))
                hrt_x += 34

#Extra comment
class GemClueDisplay:
    def __init__(self):
        bg = pg.image.load('resources/graphics/background_assets/clue_capture.png').convert_alpha()
        self.bg_W, self.bg_H = 80,94 #100w 117h
        self.bg = pg.transform.scale(bg, (self.bg_W, self.bg_H)) # 330w x 197h

        gem = pg.image.load('resources/graphics/level_graphics/coins/jewels/Jewel_0.png').convert_alpha()
        self.gem = pg.transform.scale(gem, (100, 100))

    def draw(self, gems, surface):
        x = 20
        y = mp.screen_height - 100
        g_x = 10
        g_y = y + 5

        for i in range(3):
            surface.blit(self.bg, (x,y))
            x += 90
        for i in range(gems):
            surface.blit(self.gem, (g_x, g_y))
            if  gems > 1:
                g_x += 90
