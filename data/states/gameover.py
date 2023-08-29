"""
The gameover when the player loses.
"""
import pygame as pg
from ..import prepare as mp
from ..import tools as mt


class GameOver_Menu(mt._State):
    def __init__(self):
        mt._State.__init__(self)
        self.done = False
        self.next = None
        self.cover = pg.Surface((mp.screen_size)).convert_alpha()
        self.cover.fill(0)
        self.cover_alpha = 256
        self.alpha_step  = 2
        self.display_surface = mp.SCREEN
        self.font = mp.FONTS['Silkscreen-Regular']
        self.image = mp.GFX['Gameover_screen1']
        self.image = pg.transform.scale(self.image, mp.screen_size)
        self.rect = self.image.get_rect(center=mp.SCREEN_RECT.center)
        self.files = {'compass': (100,108),
                        'map': (110,97),
                        'daBomb': (90,137)}


    def display_options(self, group):
        mt.draw_text("The Evil Banacles Devoured You!", mp.FONTS['Silkscreen-Regular'], 20, mp.SW_mid,mp.SH_qrt1+5, 'white', self.display_surface)

        txt = ["Main Menu", "Retry", "Quit"]
        x = (mp.SW_mid, mp.SW_qrt1, mp.SW_qrt3)
        y = mp.SH_mid - 30
        btn_list = []

        """
        2. level_select
        3. main_menu
        4. quit game
        """
        for i in enumerate(group):
            w_h = group.get(i[1])
            image = pg.image.load(f'resources/graphics/background_assets/{i[1]}.png')
            image = pg.transform.scale(image, w_h)
            rect = image.get_rect(center = (x[i[0]], y))
            btn = mt.ImgBtn(image, w_h, rect, self.display_surface)
            mt.draw_text(txt[i[0]], self.font, 20, x[i[0]], y-70, 'white', self.display_surface)

            btn_list.append(btn)
        """
        #main menu button
        mm_w,mm_h = 100,108
        mm = pg.image.load('resources/graphics/background_assets/compass.png')
        mm = pg.transform.scale(mm, (mm_w,mm_h))
        mm_rect = mm.get_rect(center =  (mp.SW_mid, y))
        self.mm = mt.ImgBtn(mm, (mm_w,mm_h), mm_rect, self.display_surface)
        txt = mt.draw_text("main menu", self.font, 20, x, y-25, 'white', self.display_surface)
        #overworld BUTTON
        lvl_w, lvl_h = 110,97
        lvl = pg.image.load('resources/graphics/background_assets/map.png')
        lvl = pg.transform.scale(lvl, (lvl_w, lvl_h))
        lvl_rect = lvl.get_rect(center =  (mp.SW_qrt1, y))
        self.lvl = mt.ImgBtn(lvl, (lvl_w,lvl_h), lvl_rect, self.display_surface)
        #Exit game button
        q_w,q_h = 90,137
        quit = pg.image.load('resources/graphics/background_assets/daBomb.png')
        quit = pg.transform.scale(quit, (q_w,q_h))
        q_rect = quit.get_rect(center = (mp.SW_qrt3, y-20))
        self.q = mt.ImgBtn(quit, (q_w, q_h), q_rect, self.display_surface)
        """
        return btn_list


        pass


    def get_event(self, event):
        keys = pg.key.get_pressed()
        btn_pressed = display_options(self.files)
        if event.type == pg.MOUSEBUTTONDOWN:
            if btn_pressed[0].check_clicked(mouse_pos):
                # main_menu
                self.next = "MAINMENU"
                self.done = True
            elif btn_pressed[1].check_clicked(mouse_pos):
                # retry (level_select)
                self.next = "LEVELSELECT"
                self.
                self.done  = True
            elif btn_pressed[2].check_clicked(mouse_pos):
                # quit end program
                self.next = None
                pg.quit()
                sys.exit()

    def startup(self, current_time, persistant):
        """Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time."""
        self.persist = persistant
        self.start_time = current_time
        pass

    def cleanup(self):
        """Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False."""
        self.done = False
        return self.persist
        pass

    def update(self, surface, keys, current_time, time_delta):
        self.current_time = current_time
        surface.blit(self.image, self.rect)
        self.display_options(self.files)
