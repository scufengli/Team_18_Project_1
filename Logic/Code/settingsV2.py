import pygame
vertical_tile_number = 11 
tile_size = 64

screen_height = vertical_tile_number*tile_size
screen_width = 1200

SH_qrt1 = screen_height/4
SH_mid, SH_qrt3 = SH_qrt1*2,SH_qrt1*3
SW_qrt1 = screen_width/4
SW_mid, SW_qrt3 = SW_qrt1*2,SW_qrt1*3

body1_font = '../Graphics/fonts/IndieFlower-Regular.ttf'
TITLE_font = '../Graphics/fonts/Kablammo-Regular.ttf'
BLACK, WHITE = (217,17,114), (255,235,90)

def draw_text( text, font_type, size, x, y, color, display_surface):
        font = pygame.font.Font(font_type, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        display_surface.blit(text_surface, text_rect)
        return text_rect
