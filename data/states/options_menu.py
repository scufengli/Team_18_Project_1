#OPTIONS
import pygame as pg

from .. import prepare as mp # Module prepare
from .. import tools as mt # Module tools
from .gameplay_data import player

class Option_Menu(mt._State):
    """Options menu that can be called from any state"""
    def __init__(self):
        mt._State.__init__(self)
        self.next = None
        self.cover = pg.Surface((mp.screen_size)).convert_alpha()
        self.cover.fill(0)
        self.cover_alpha = 256
        self.alpha_step  = 2
        self.display_surface = mp.SCREEN

        #BG & TXT
        self.title_font = mp.FONTS['Kablammo-Regular']
        self.header_font = mp.FONTS['Milonga-Regular']
        self.sub_font = mp.FONTS['Milonga-Regular']
        self.color1 = (45, 188, 214 ) # grass green 101, 152, 0
        self.color2 = (132, 90, 61) #cyan (144, 70, 20) # brown 45, 188, 214
        self.color3 = (82, 117, 87) # green 40, 158,57
        self.color4 = (73, 166, 166 ) # 73, 166, 166 darker cyan blue
        self.image = mp.BackGroundGFX['scroll_bg']
        self.image = pg.transform.scale(self.image,(mp.screen_width, mp.screen_height))
        self.rect = self.image.get_rect(center=mp.SCREEN_RECT.center)
        self.mus_x, self.mus_y = mp.SW_qrt1-20, mp.SH_qrt1+50
        self.ctrl_x, self.ctrl_y = mp.SW_qrt3, mp.SH_qrt1+50

        #BUTTON IMAGES
        w, h = 67,67
        green_btn = pg.image.load('resources/graphics/background_assets/green_on.png')
        self.green_btn = pg.transform.scale(green_btn,(w, h))
        gold_btn = pg.image.load('resources/graphics/background_assets/gold_off.png')
        self.gold_btn = pg.transform.scale(gold_btn,(w, h))
        back_btn = pg.image.load('resources/graphics/background_assets/wheel.png')
        self.back_btn = pg.transform.scale(back_btn, (70, 74))

        w2,h2 = 300,93
        left = pg.image.load('resources/graphics/background_assets/left_arrow.png')
        right = pg.image.load('resources/graphics/background_assets/right_arrow.png')
        spbar = pg.image.load('resources/graphics/background_assets/spacebar.png')
        down =  pg.image.load('resources/graphics/background_assets/down_arrow.png')
        self.left = pg.transform.scale(left,(w, h+6))
        self.right = pg.transform.scale(right,(w, h+6))
        self.down = pg.transform.scale(down,(w, h+6))
        self.spbar = pg.transform.scale(spbar,(w2, h2))


        #INTERACTIVES
        #----MUSIC
        self.music_status = 'on'
        self.bgm = mp.MUSIC['main_menu_BG_music']
        #----back

    def draw(self):
        #BG display
        center_x, center_y = self.rect.center
        top_x, top_y, w, h = self.image.get_bounding_rect()
        self.display_surface.blit(self.image,self.rect)
        sub_size = 40

        title = mt.draw_text("Options", self.title_font, 70, center_x, top_y+125, self.color4, self.display_surface)

        volume_txt = mt.draw_text('Music', self.header_font,sub_size, self.mus_x, self.mus_y, self.color1, self.display_surface)
        on_txt = mt.draw_text('ON', self.sub_font,sub_size-10, self.mus_x+30, mp.SH_mid-20, self.color3, self.display_surface)
        off_txt = mt.draw_text('OFF', self.sub_font,sub_size-10, self.mus_x+30, mp.SH_mid+77, self.color3, self.display_surface)

        x,y = 0, mp.SH_mid
        ctrl_txt =  mt.draw_text('Controls', self.header_font,sub_size, self.ctrl_x, self.ctrl_y, self.color1, self.display_surface)
        spacebar = self.display_surface.blit(self.spbar, (self.ctrl_x-150, y-60))
        mt.draw_text('spacebar', self.sub_font, sub_size-10,self.ctrl_x,y-20, self.color3, self.display_surface)
        self.display_surface.blit(self.right, (self.ctrl_x + 80, y+50))
        self.display_surface.blit(self.left, (mp.SW_mid+150 , y+50))
        self.display_surface.blit(self.down, (mp.SW_qrt3-30, mp.SH_mid+120))
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
        on_x, on_y = self.mus_x-80, mp.SH_mid-20
        off_x, off_y = self.mus_x-80, mp.SH_mid+77
        back_x, back_y = self.rect.center

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

        back_rect = pg.draw.circle(self.display_surface, 'yellow', (back_x,back_y), 20, 0)
        mt.draw_text("Return", self.sub_font, 15, back_x, back_y+50, self.color1, self.display_surface)
        back = myBtn(self.back_btn, (back_x,back_y), back_rect, self.display_surface)

        return [on_btn, off_btn, back]

    def get_event(self, event):
        mouse_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        btn_pressed = self.music_ctrl(self.music_status)
        if event.type == pg.MOUSEBUTTONDOWN:
            if btn_pressed[0].check_clicked(mouse_pos):
                # Music is on
                self.music_status = 'on'
                pg.mixer.music.unpause()

            elif btn_pressed[1].check_clicked(mouse_pos):
                # Music is off
                self.music_status = 'off'
                pg.mixer.music.pause()
            elif btn_pressed[2].check_clicked(mouse_pos):
                #end states
                self.next = self.previous
                self.done = True

    def startup(self, current_time, persistant):
        self.persist = persistant
        self.start_time = current_time
        """Load and play the music on scene start."""
        #pg.mixer.init()
        #pg.mixer.music.set_volume(0.7)
        #pg.mixer.music.load(self.bgm)
        pg.mixer.music.unpause()

        return mt._State.startup(self, current_time, persistant)

    def update(self, surface, keys, current_time, time_delta):
        """Update function for state.  Must be overloaded in children."""
        self.current_time = current_time
        surface.blit(self.image,self.rect)
        mouse_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        self.draw()
        self.music_ctrl(self.music_status)
        pg.draw.circle(self.display_surface,'green',mouse_pos,10)

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
