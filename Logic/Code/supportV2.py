from csv import reader
from os import walk
from settingsV2 import tile_size
import pygame


def import_folder(path):
    surface_list = []
    for _,__,image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image_files
            image_surf = pygame.image.load(full_path).convert_alpha()

    return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x, y = col * tile_size, row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), flags= pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x,y,tile_size, tile_size))
            cut_tiles.append(new_surf)
    
    return cut_tiles

def draw_text( text, font_type, size, x, y, color, display_surface):
    font = pygame.font.Font(font_type, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    display_surface.blit(text_surface, text_rect)
