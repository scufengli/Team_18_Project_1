import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.qrt1_w, self.qrt1_h = self.mid_w/2, self.mid_h/2
        self.qrt3_w, self.qrt3_h = (self.mid_w + self.qrt1_w), (self.mid_h + self.qrt1_h)
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -90
        self.sub_font = 'fonts/Handjet-Regular.ttf'
        self.bg_img = pygame.image.load('art_assets/Background_Assets/OceanBG1.jpeg')
        self.bg_img = pygame.transform.scale(self.bg_img,(self.game.DISPLAY_W, self.game.DISPLAY_H))

    def draw_cursor(self):
        self.game.draw_text("X", self.game.TITLE_font, 25, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        #self.game.window.blit(self.game.display, (0,0))
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w+5, self.mid_h
        self.optionsx, self.optionsy = self.qrt1_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.qrt3_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.startx + self.offset-40, self.starty)


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            #self.game.display.fill(self.game.BLACK)
            #self.game.window.blit(self.game.bg_img, (0,0))
            self.game.display.blit(self.bg_img, (0,0))
            self.game.draw_text("Cult of the Barnacle", self.game.TITLE_font, 80, self.game.DISPLAY_W/2, 80)
            self.game.draw_text("Start Game", self.game.body1_font, 40, self.startx, self.starty)
            self.game.draw_text("Options", self.game.body1_font, 40, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", self.game.body1_font, 40, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.game.check_events()
            self.check_input()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset-40, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.startx + self.offset-40, self.starty)
                self.state = "Start"

        if self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
            elif self.state == "Credits":
                self.game.curr_menu = self.game.cr_menu
            elif self.state == "Options":
                self.game.curr_menu = self.game.op_menu
            self.run_display = False

class OptionMenu(Menu):
    """docstring for OptionsMenu."""

    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            #self.game.display.fill((0,0,0))
            self.game.display.blit(self.bg_img, (0,0))
            self.game.draw_text("Options", self.sub_font, 40, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2-30)
            self.game.draw_text("Volume", self.sub_font, 40, self.volx, self.voly+10)
            self.game.draw_text("Controls", self.sub_font, 40, self.controlsx, self.controlsy+20)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY or self.game.BACK_KEY:
            self.game.curr_menu = self.game.m_menu
            self.run_display = False

        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == "Volume":
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy+20)
                self.state = "Controls"
            elif self.state == "Controls":
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly+10)
                self.state = "Volume"
        elif self.game.START_KEY:
            ## TODO: create a volume menu and a controls menu
            pass

class CreditsMenu(Menu):
    """docstring for CreditsMenu."""

    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.m_menu
                self.run_display = False
            #self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.bg_img, (0,0))
            self.game.draw_text("Credits:", self.sub_font, 40, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2-20)
            self.game.draw_text("Apalapa: TechWise Talentsprint Cohort II", self.sub_font, 40, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2+30)
            self.blit_screen()
