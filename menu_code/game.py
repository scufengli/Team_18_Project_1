import pygame
#import url('https://fonts.googleapis.com/css2?family=Kablammo&family=Palanquin:wght@300&family=Poiret+One&display=swap');
from start_menu import *

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.BACK_KEY, self.START_KEY = False,False,False, False

        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))


        self.body1_font = 'fonts/IndieFlower-Regular.ttf'
        self.TITLE_font = 'fonts/Kablammo-Regular.ttf'
        self.BLACK, self.WHITE = (217,17,114), (255,235,90)
        #self.bg_img = pygame.image.load('apalapaArt/Background_Assets/OceanBG1.jpeg')
        #self.bg_img = pygame.transform.scale(self.bg_img,(self.DISPLAY_W, self.DISPLAY_H))

        self.m_menu = MainMenu(self)
        self.op_menu = OptionMenu(self)
        self.cr_menu = CreditsMenu(self)
        self.curr_menu = self.m_menu

        #self.inven_view = Inventory()

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.draw_text("Thanks for Playing", self.TITLE_font, 40, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.BACK_KEY, self.START_KEY = False, False, False, False

    def draw_text(self, text, font_type, size, x, y):
        font = pygame.font.Font(font_type, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)
