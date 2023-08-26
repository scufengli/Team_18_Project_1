"""
This module initializes the display and creates dictionaries of resources.
"""

import os
import pygame as pg
from . import tools

vertical_tile_number = 11 
tile_size = 64

screen_height = vertical_tile_number*tile_size
screen_width = 1200
screen_size = (screen_width, screen_height )

SH_qrt1 = screen_height/4
SH_mid, SH_qrt3 = SH_qrt1*2,SH_qrt1*3
SW_qrt1 = screen_width/4
SW_mid, SW_qrt3 = SW_qrt1*2,SW_qrt1*3

ORIGINAL_CAPTION = "Cult of the Barnacle"


#Initialization
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(screen_size)
SCREEN_RECT = SCREEN.get_rect()


#Resource loading (Fonts and music just contain path names).

#===== // // // UNCOMMENT WHEN FOLDERS ARE ORGANIZED PROPERLY // // // =====#

# SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))

#===== // // // UNCOMMENT WHEN FOLDERS ARE ORGANIZED PROPERLY // // // =====#

FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
BackGroundGFX   = tools.load_all_gfx(os.path.join("resources", "graphics", "background_assets"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
AniDict = tools.load_animations_from_folders('character')


