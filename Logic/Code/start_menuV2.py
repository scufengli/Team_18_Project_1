import pygame, sys
from settingsV2 import*
from levelV2 import Level
from game_data import level_0
from start_menuV2 import*

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)

class Menu():
    def __init__(self,display_surface):
        self.display_surface = display_surface
        self.bg = pygame.image.load('../Graphics/Background_Assets/OceanBG1.jpeg')
        self.bg = pygame.transform.scale(self.bg,(screen_width, screen_height))

    def get_input(self,display_surface):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            print("Key RIGHT")
        elif keys[pygame.K_LEFT]:
            print("Key LEFT")
        elif keys[pygame.K_DOWN]:
            print("Key DOWN")
        elif keys[pygame.K_UP]:
            print("Key UP")
        if keys[pygame.K_SPACE]:
            print("Key SPACE")
        else:
            pass

    def display_menus(self,):
        draw_text("Cult of the Barnacle,", TITLE_font,80,SW_mid,80,'white',self.display_surface)
        Button1 = draw_text("Start Game", body1_font,40,SW_mid+5,SH_mid,'white',self.display_surface)
        Button2 = draw_text("Options", body1_font,40,SW_qrt1,SH_mid+50,'white',self.display_surface)
        Button3 = draw_text("Credits", body1_font,40,SW_qrt3,SH_mid+50,'white',self.display_surface)
        return [Button1, Button2, Button3]
    
    def run(self):
        self.display_surface.blit(self.bg,(0,0))
        Blist = self.display_menus()
        self.get_input(self.display_surface)
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(self.display_surface,'green',mouse_pos,10)
        # for button in Blist:
        #     if button.collidepoint(mouse_pos):
        #         pygame.draw.circle(self.display_surface,'blue',mouse_pos,10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if Blist[0].collidepoint(mouse_pos):
                    self.display_surface.fill('white')


class MainMenu(Menu):
    def __init__(self,display_surface):
        super.__init__(self,display_surface)

    








