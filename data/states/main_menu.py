"""
This module contains our intro state with the movie.
"""

import pygame as pg

from .. import prepare as mp # Module prepare
from .. import tools as mt # Module tools

class Main_Menu(mt._State):
    """ Main menu that starts up after the splash screen."""
    def __init__(self):
        mt._State.__init__(self)
        self.next = None
        self.cover = pg.Surface((mp.screen_size)).convert_alpha()
        self.cover.fill(0)
        self.cover_alpha = 256
        self.alpha_step  = 2
        self.title_font = mp.FONTS['Kablammo-Regular']
        self.sub_font = mp.FONTS['IndieFlower-Regular']
        self.yellow = (255,235,90)
        self.display_surface = mp.SCREEN
        self.image = mp.BackGroundGFX['OceanBG1']
        self.image = pg.transform.scale(self.image,(mp.screen_width, mp.screen_height))
        self.rect = self.image.get_rect(center=mp.SCREEN_RECT.center)
        self.Blist = self.display_menus()

        self.bgm = mp.MUSIC['main_menu_BG_music']

    def draw_text(self, text, font_type, size, x, y, color, display_surface):
        font = pg.font.Font(font_type, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        display_surface.blit(text_surface, text_rect)
        return text_rect

    def startup(self, current_time, persistant):
        """Load and play the music on scene start."""
        pg.mixer.music.load(self.bgm)
        pg.mixer.music.play(-1)
        return mt._State.startup(self, current_time, persistant)

    def display_menus(self,):
        StartGameIcon = mt.Button((20, mp.SW_mid,80), "Cult of the Barnacle", (mp.FONTS['Kablammo-Regular']), 80, 'white', 'white', self.display_surface)
        start_game = mt.Button((mp.SW_mid+5,mp.SH_mid), 'Start Game',(mp.FONTS['IndieFlower-Regular']),40,'white', 'red', self.display_surface)
        options = mt.Button((mp.SW_qrt1,mp.SH_mid+50), 'Options',(mp.FONTS['IndieFlower-Regular']), 40, 'white', 'red', self.display_surface)
        credits = mt.Button((mp.SW_qrt3,mp.SH_mid+50), 'Credits',(mp.FONTS['IndieFlower-Regular']),40 ,'white', 'red', self.display_surface)
        return [start_game, options, credits, StartGameIcon]
        
    def update(self, surface, keys, current_time, time_delta):
        self.current_time = current_time
        surface.blit(self.image,self.rect)
        self.cover.set_alpha(self.cover_alpha)
        self.cover_alpha = max(self.cover_alpha-self.alpha_step,0)
        surface.blit(self.cover,(0,0))
        mouse_pos = pg.mouse.get_pos()
        pg.draw.circle(self.display_surface,'green',mouse_pos,10)
        self.display_menus()

        for button in self.Blist:
            button.change_color(mouse_pos)
            button.update(self.display_surface)

    def get_event(self, event):
        """Get events from Control. Currently changes to next state on any key
        press."""
        mouse_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.Blist[0].check_for_input(mouse_pos):
                # play()
                self.next = "GAMEPLAY"
                self.done = True
                pass
            if self.Blist[1].check_for_input(mouse_pos):
                # options()
                #self.next = "OPTIONS"
                #self.done = True
                pass
            if self.Blist[2].check_for_input(mouse_pos):
                # credits()
                #self.next = "CREDITS"
                #self.done = True
                pass

    def cleanup(self):
        """Stop the music when scene is done."""
        pg.mixer.music.stop()
        return mt._State.cleanup(self)
