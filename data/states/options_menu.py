#OPTIONS
import pygame as pg

from .. import prepare as mp # Module prepare
from .. import tools as mt # Module tools
from ...Platformer.Code import player

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
        self.header_font = mp.FONTS['Milonga-Regular']
        self.sub_font = mp.FONTS['IndieFlower-Regular']
        self.yellow = (255,235,90)
        self.image = mp.BackGroundGFX['scroll_bg']
        self.image = pg.transform.scale(self.image,(mp.screen_width, mp.screen_height))
        self.rect = self.image.get_rect(center=mp.SCREEN_RECT.center)
        self.mus_x, self.mus_y = mp.SW_qrt1-20, mp.SH_qrt1
        self.ctrl_x, self.ctrl_y = mp.SW_qrt3, mp.SH_qrt1

        #BUTTON IMAGES
        w, h = 67,67
        green_btn = pg.image.load('resources/graphics/background_assets/green_on.png')
        self.green_btn = pg.transform.scale(green_btn,(w, h))
        gold_btn = pg.image.load('resources/graphics/background_assets/gold_off.png')
        self.gold_btn = pg.transform.scale(gold_btn,(w, h))

        #INTERACTIVES
        #----MUSIC
        self.music_status = 'on'
        self.bgm = mp.MUSIC['main_menu_BG_music']
        #----PLAYER
        self.player = pg.sprite.Group()

    def draw(self):
        #BG display
        center_x, center_y = self.rect.center
        top_x, top_y, w, h = self.image.get_bounding_rect()
        self.display_surface.blit(self.image,self.rect)
        sub_size = 40

        title = mt.draw_text("Options", self.title_font, 60, center_x, top_y+25, self.yellow, self.display_surface)
        volume_txt = mt.draw_text('Music', self.header_font,sub_size, self.mus_x, self.mus_y, 'blue', self.display_surface)
        on_txt = mt.draw_text('ON', self.sub_font,sub_size, self.mus_x, mp.SH_mid-60, 'black', self.display_surface)

        off_txt = mt.draw_text('OFF', self.sub_font,sub_size, self.mus_x, mp.SH_mid+57, 'black', self.display_surface)
        ctrl_txt =  mt.draw_text('Controls', self.header_font,sub_size, self.ctrl_x, self.ctrl_y, 'blue', self.display_surface)
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

    def music_ctrl(self, status):
        self.music_status = status
        on_x, on_y = self.mus_x-80, mp.SH_mid-60
        off_x, off_y = self.mus_x-80, mp.SH_mid+57

        if self.music_status == 'on':
            on_img = self.green_btn
            off_img = self.gold_btn
        else:
            on_img = self.gold_btn
            off_img = self.green_btn

        on_rect = pg.draw.circle(self.display_surface, 'black',(on_x, on_y), 34, 57)
        on_btn = myBtn(on_img,(on_x, on_y), on_rect, self.display_surface)

        off_rect = pg.draw.circle(self.display_surface, 'black',(off_x, off_y), 34, 57)
        off_btn = myBtn(off_img,(off_x, off_y), off_rect, self.display_surface)

        return [on_btn, off_btn]

    def get_event(self, event):
        mouse_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        btn_pressed = self.music_ctrl(self.music_status)
        if event.type == pg.MOUSEBUTTONDOWN:
            if btn_pressed[0].check_clicked(mouse_pos):
                # Music is on
                self.music_status = 'on'
                pg.mixer.music.unpause()

            if btn_pressed[1].check_clicked(mouse_pos):
                # Music is off
                self.music_status = 'off'
                pg.mixer.music.pause()
            #return self.music_status
                pass
        if  event.type == pg.KEYDOWN:
            #Player
            pass
        #return key press
        else:
            pass

    def startup(self, current_time, persistant):
        self.persist = persistant
        self.start_time = current_time
        """Load and play the music on scene start."""
        pg.mixer.init()
        pg.mixer.music.set_volume(0.7)
        pg.mixer.music.load(self.bgm)
        pg.mixer.music.play(-1)

        return mt._State.startup(self, current_time, persistant)

    def update(self, surface, keys, current_time, time_delta):
        """Update function for state.  Must be overloaded in children."""
        self.current_time = current_time
        self.cover.set_alpha(self.cover_alpha)
        self.cover_alpha = max(self.cover_alpha-self.alpha_step,0)
        surface.blit(self.cover,(0,0))
        mouse_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        pg.draw.circle(self.display_surface,'green',mouse_pos,10)
        self.draw()
        self.music_ctrl(self.music_status)
        self.player.update()
        self.player.draw(self.display_surface)

    def cleanup(self):
        """Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False."""
        #self.done = False
        #return self.persist
        return mt._State.cleanup(self)

class myBtn():
    def __init__(self, image, pos, rect, display):
        x, y = pos
        self.rect = rect
        display.blit(image, image.get_rect(center = self.rect.center))

    def check_clicked(self,position):
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)
