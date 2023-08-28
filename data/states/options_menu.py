#OPTIONS
import pygame as pg

from .. import prepare as mp # Module prepare
from .. import tools as mt # Module tools
from .gameplay_data import player

class Option_Menu(mt._State):
    """Options menu that can be called from any state"""
    def __init__(self): #WHERE SHOULD I PASS MUSIC FROM LAST STATE
        mt._State.__init__(self)
        self.next = None
        self.cover = pg.Surface((mp.screen_size)).convert_alpha()
        self.cover.fill(0)
        self.cover_alpha = 256
        self.alpha_step  = 2
        self.display_surface = mp.SCREEN

        #BG & TXT
        self.title_font = mp.FONTS['Handjet-Regular']
        self.sub_font = mp.FONTS['IndieFlower-Regular']
        self.yellow = (255,235,90)
        self.image = mp.BackGroundGFX['scroll_bg']
        self.image = pg.transform.scale(self.image,(mp.screen_width, mp.screen_height))
        self.rect = self.image.get_rect(center=mp.SCREEN_RECT.center)
        self.mus_x, self.mus_y = mp.SW_qrt1-20, mp.SH_qrt1
        self.ctrl_x, self.ctrl_y = mp.SW_qrt3, mp.SH_qrt1
        #BUTTON IMAGES
        self.on_btn = pg.image.load('resources/graphics/background_assets/green_on.png')
        #self.on_btn = pg.transform.scale(self.on_btn,(w, h))
        #self.on_btn = on_btn.get_rect().center
        self.off_btn = pg.image.load('resources/graphics/background_assets/gold_off.png')
        #self.on_btn = pg.transform.scale(self.off_btn,(w, h))
        #self.off_btn = off_btn.get_rect().center

        #INTERACTIVES
        self.Blist = self.draw()
        #----MUSIC
        #----PLAYER
        self.player = pg.sprite.GroupSingle()




    def draw(self):
        center_x, center_y = self.rect.center
        top_x, top_y, w, h = self.image.get_bounding_rect()
        self.display_surface.blit(self.image,self.rect)
        sub_size = 40

        title = mt.draw_text("Options", self.title_font, 60, center_x, top_y+25, self.yellow, self.display_surface)
        volume_txt = mt.draw_text('Music', self.sub_font,sub_size, self.mus_x, self.mus_y, 'black', self.display_surface)
        on_txt = mt.draw_text('ON', self.sub_font,sub_size, self.mus_x, mp.SH_mid-60, 'black', self.display_surface)
        off_txt = mt.draw_text('OFF', self.sub_font,sub_size, self.mus_x, mp.SH_mid+57, 'black', self.display_surface)
        ctrl_txt =  mt.draw_text('Controls', self.sub_font,sub_size, self.ctrl_x, self.ctrl_y, 'black', self.display_surface)
        """
        music_on = mt.Button()
        music_off =
        """
        """
        ctrl_btns = #function w/ for loop through file of photos
        player = #blit player class w/ check input
        """

        pass

    def player_ctrl(self):
        """
        self.player = Player(self.rect.center)
        self.player.draw(self.display_surface)
        """
        pass

    def music_ctrl(self):
        #pygame.draw.circle(surface, color, (center), radius, width)
        #on_rect = pg.draw.circle(self.display_surface, 'yellow',(self.mus_x-80, mp.SH_mid-60), 34, 67)
        on_btn = mt.Button((self.mus_x-80, mp.SH_mid-60),None, None, None, None,None, self.display_surface, self.on_btn)
        #off_rect = pg.draw.circle(self.display_surface, 'yellow',(self.mus_x-80, mp.SH_mid+57), 34, 67)
        off_btn = mt.Button((self.mus_x-80, mp.SH_mid-60),None, None, None, None, None, self.display_surface, self.off_btn)
        return [on_btn, off_btn]

    def get_event(self, event):
        mouse_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.Blist[0].check_for_input(mouse_pos):
                # Music
                #self.next = "LEVELSELECT"
                #self.done = True
                pass
            if self.Blist[1].check_for_input(mouse_pos):
                # Character()
                #self.next = "OPTIONS"
                #self.done = True
                pass
            if self.Blist[2].check_for_input(mouse_pos):
                # previous()
                #self.next = "CREDITS"
                #self.done = True
                pass
        if  event.type == pg.KEYDOWN:
            #Player
            pass
        pass

    def startup(self, current_time, persistant):
        """Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time."""
        self.persist = persistant
        self.start_time = current_time
        pass

    def cleanup(self):
        """Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False."""
        #self.done = False
        #return self.persist
        pass

    def update(self, surface, keys, current_time, time_delta):
        """Update function for state.  Must be overloaded in children."""
        self.current_time = current_time
        #surface.blit(self.image,self.rect)
        self.cover.set_alpha(self.cover_alpha)
        self.cover_alpha = max(self.cover_alpha-self.alpha_step,0)
        self.draw()
        surface.blit(self.cover,(0,0))
        mouse_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        pg.draw.circle(self.display_surface,'green',mouse_pos,10)
        #self.display_menus()
        self.music_ctrl()
        self.player.update()
        self.player.draw(self.display_surface)
        pass

    def cleanup(self):
        return mt._State.cleanup(self)
