import pygame
from supportV2 import *
from settingsV2 import tile_size
from tilesV2 import *


class Level:
    def __init__(self,level_data, surface):
        # GENERAL SETUP
        self.display_surface = surface
        self.world_shift = -1

        #TERRAIN SETUP
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        #PLAYER SET UP
        player_layout = import_csv_layout(level_data['Player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
    
    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x,y = col_index * tile_size, row_index*tile_size
                if val == '0':
                    print('Player Goes Here')
                if val == '1':
                    hat_surface = pygame.image.load('../Graphics/ms_tan/stand_0.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)


    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x,y = col_index * tile_size, row_index*tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('../Graphics/Terrain/terrain.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y, tile_surface)
                        sprite_group.add(sprite)

        return sprite_group
    

    def run(self):
        # RUNS THE AN ENTIRE LEVEL 
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # PLAYER SPRITES 
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)