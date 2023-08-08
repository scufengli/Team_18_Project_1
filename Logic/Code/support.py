from os import walk
from csv import reader
import pygame

# # =========== TEST IMPORT FOLDER FUNCTION FOR TROUBLE SHOOTING ===========
# character_path = '../Graphics/Character/Run'
# def import_folder(path):
#     for x,y,z in walk(path):
#         print(x,y,z)

# import_folder(character_path)
# # =========== END TEST IMPORT FOLDER FUNCTION FOR TROUBLE SHOOTING ===========


# ========== DELETE ABOVE CODE WHEN GAME IS COMPLETE ==========
def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image 
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map