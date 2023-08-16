import pygame, sys
from settingsV2 import*
from levelV2 import Level
from game_data import level_0
from start_menuV2 import*
from supportV2 import*

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

level = Level(level_0,screen)

class MainMenu():
    def __init__(self,display_surface):
        self.display_surface = display_surface
        self.bg = pygame.image.load('../Graphics/Background_Assets/OceanBG1.jpeg')
        self.bg = pygame.transform.scale(self.bg,(screen_width, screen_height))

        

    def display_menus(self,):
        draw_text("Cult of the Barnacle,", TITLE_font,80,SW_mid,80,'white',self.display_surface)

        # Button1 = draw_text("Start Game", body1_font,40,SW_mid+5,SH_mid,'white',self.display_surface)
        # Button2 = draw_text("Options", 
        # body1_font,40,SW_qrt1,SH_mid+50,'white',self.display_surface)
        # Button3 = draw_text("Credits", body1_font,40,SW_qrt3,SH_mid+50,'white',self.display_surface)

        start_game = Button((SW_mid+5,SH_mid), 'Start Game',body1_font,40,'white', 'red', self.display_surface)

        options = Button((SW_qrt1,SH_mid+50), 'Options',body1_font,40, 'white', 'red', self.display_surface)
        
        credits = Button((SW_qrt3,SH_mid+50), 'Start Game',body1_font,40,'white', 'red', self.display_surface)

        return [start_game, options, credits]
    
    def run(self, event_type):
        self.display_surface.blit(self.bg,(0,0))
        Blist = self.display_menus()
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(self.display_surface,'green',mouse_pos,10)

        for button in Blist:
            button.change_color(mouse_pos)
            button.update(self.display_surface)

        if event_type == pygame.MOUSEBUTTONDOWN:
            if Blist[0].check_for_input(mouse_pos):
                # play()
                return True
                pass
            if Blist[1].check_for_input(mouse_pos):
                # options()
                pass
            if Blist[2].check_for_input(mouse_pos):
                # credits()
                pass
            

        # self.get_input(self.display_surface)



    # def get_input(self,display_surface):

    #     keys = pygame.key.get_pressed()

    #     if keys[pygame.K_RIGHT]:
    #         print("Key RIGHT")
    #     elif keys[pygame.K_LEFT]:
    #         print("Key LEFT")
    #     elif keys[pygame.K_DOWN]:
    #         print("Key DOWN")
    #     elif keys[pygame.K_UP]:
    #         print("Key UP")
    #     if keys[pygame.K_SPACE]:
    #         print("Key SPACE")
    #     else:
    #         pass







