import pygame as pg
from ... import prepare as mp
from ... import tools as mt

import pygame
from .tilesV2 import *
from .decorations import *
from .enemy import*
from .player import Player



class Level:
    def __init__(self,level_data, surface):
        # GENERAL SETUP
        self.display_surface = surface
        self.world_shift = 0
        #TERRAIN SETUP
        terrain_layout = mt.import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        # COINS ========== CREATE COINS IMAGE ==========
        coin_layout = mt.import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coin')
        self.coin_total = 0

        # # CHEST ========== CREATE CHEST IMAGE ==========
        # chest_layout = import_csv_layout(level_data['chest'])
        # self.chest_sprites = self.create_tile_group(chest_layout,'chest')


        # # ENEMIES ========== CREATE ENEMIES IMAGE ==========
        # enemy_layout = import_csv_layout(level_data['Enemies'])
        # self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # # CONSTRAINTS ========== CREATE CONSTRAINTS IMAGE ==========
        # constraint_layout = import_csv_layout(level_data['constraints'])
        # self.constraint_layout = self.create_tile_group(constraint_layout, 'constraints')

        #PLAYER SET UP
        player_layout = mt.import_csv_layout(level_data['Player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)


        # DECORATIONS
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * mp.tile_size
        self.water = Water(mp.screen_height - 20, level_width)
        self.clouds = Clouds(400,level_width, 20)

    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x,y = col_index * mp.tile_size, row_index*mp.tile_size
                if val == '0':
                    sprite = Player((x,y))
                    self.player.add(sprite)


    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()


        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x,y = col_index * mp.tile_size, row_index*mp.tile_size
                    if type == 'terrain':
                        terrain_tile_list = mt.import_cut_graphic('resources/graphics/level_graphics/terrain/tileset.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(mp.tile_size,x,y, tile_surface)
                        sprite_group.add(sprite)
                        continue

                    if type == 'coins':
                        #sprite = Coin(tile_size,x,y,'../Graphics/coins')
                        continue
                        pass

                    # CODE TO CHANGE THE COLOR OF COINS
                    if val == '0':
                        sprite = Coin(mp.tile_size,x,y,'resources/graphics/level_graphics/coins/gold')
                        #self.coin_positions(x,y)
                        sprite_group.add(sprite)
                        continue

                    if val == '1':
                        sprite = Coin(mp.tile_size,x,y,'resources/graphics/level_graphics/coins/silver')
                        sprite_group.add(sprite)

                        continue
        # =============== UNCOMMENT WHEN IMAGES ARE CREATED ==========================


                            # if type == 'enemies':
                            #     sprite = Enemy(tile_size,x,y)

                            # if type == 'constrains':
                            #     sprite = Tile(tile_size,x,y)


        # =============== UNCOMMENT WHEN IMAGES ARE CREATED ==========================

        return sprite_group

    # =============== UNCOMMENT WHEN IMAGES ARE CREATED ==========================
        # def enemy_collision_reverse(self):
        #     for enemy in self.enemy_sprites.sprites():
        #         if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
        #             enemy.reverse()

    # =============== UNCOMMENT WHEN IMAGES ARE CREATED ==========================


    def horizontal_movement_collision(self):
        player = self.player.sprite

        # if player.status == "Crouch_Walk" and self.world_shift == 0:
        #     player.speed = 2
        # else:
        #     player.speed = 8

        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x <0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0 :
                    player.rect.right = sprite.rect.left
                    player.on_Right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >=0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <=0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    #COIN COLLISION
    def coin_collection(self):
        player = self.player.sprite

        for coin in self.coin_sprites.sprites():
            if player.rect.colliderect(coin.rect):
                    pygame.sprite.Sprite.remove(coin, self.coin_sprites)
                    self.coin_total += 1



    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < int(mp.screen_width/4) and direction_x < 0:
            if player.status == "Crouch_Walk":
                self.world_shift = 2
                player.speed = 0
            else:
                self.world_shift = 8
                player.speed = 0
        elif player_x > int(mp.screen_width*3/4) and direction_x > 0:
            if player.status == "Crouch_Walk":
                self.world_shift = 2
                player.speed = 0
            else:
                self.world_shift = -8
                player.speed = 0
        else:
            if player.status == "Crouch_Walk":
                self.world_shift = 0
                player.speed = 2
            else:
                self.world_shift = 0
                player.speed = 8

    def run(self):
        # RUNS THE AN ENTIRE LEVEL

        # DECORATIONS
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # TERRAIN
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

# ============== UNCOMMENT WHEN IMAGES ARE CREATED =========================

        # COINS
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        print(self.coin_total)

        # # ENEMIES
        # self.enemy_sprites.update(self.world_shift)
        # self.constraint_sprites.update(self.world_shift)
        # self.enemy_collision_reverse()
        # self.enemy_sprites.draw(self.world_shift)

        # # CHEST
        # self.chest_sprites.update(self.world_shift)
        # self.chest_sprites.draw(self.display_surface)

        # self.water.update(self.world_shift)
        # self.water.draw(self.display_surface)

# =============== UNCOMMENT WHEN IMAGES ARE CREATED ==========================

        # PLAYER SPRITES
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.coin_collection()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
