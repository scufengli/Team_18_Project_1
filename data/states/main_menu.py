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
    def draw_text(self, text, font_type, size, x, y, color, display_surface):
        font = pg.font.Font(font_type, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        display_surface.blit(text_surface, text_rect)
        return text_rect

    def startup(self, current_time, persistant):
        """Load and play the music on scene start."""        
        return mt._State.startup(self, current_time, persistant)

    def display_menus(self,):
        StartGameIcon = mt.Button((mp.SW_qrt1-80,20,80), "Cult of the Barnacle", self.title_font, 80, self.yellow, self.yellow, self.display_surface, None)
        start_game = mt.Button((mp.SW_mid-90,mp.SH_mid-20), 'Start Game',self.sub_font,40,self.yellow, 'red', self.display_surface, None)
        options = mt.Button((mp.SW_qrt1-80,mp.SH_mid+50), 'Options',self.sub_font, 40, self.yellow, 'red', self.display_surface, None)
        credits = mt.Button((mp.SW_qrt3-20,mp.SH_mid+50), 'Credits',self.sub_font,40 ,self.yellow, 'red', self.display_surface, None)
        return [start_game, options, credits, StartGameIcon]

    def update(self, surface, keys, current_time, time_delta):
        self.current_time = current_time
        surface.blit(self.image,self.rect)
        self.cover.set_alpha(self.cover_alpha)
        self.cover_alpha = max(self.cover_alpha-self.alpha_step,0)
        surface.blit(self.cover,(0,0))
        self.persist['water_level_done'] = [False,False,False, False, False]
        mouse_pos = pg.mouse.get_pos()
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
                self.next = "LEVELSELECT"
                self.done = True
            if self.Blist[1].check_for_input(mouse_pos):
                # options()
                self.next = "OPTIONS"
                self.done = True
            if self.Blist[2].check_for_input(mouse_pos):
                # credits()
                #self.next = "CREDITS"
                #self.done = True
                pass

    def cleanup(self):
        """Stop the music when scene is done."""
        #pg.mixer.music.pause()
        return mt._State.cleanup(self)
