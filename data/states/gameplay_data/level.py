import pygame as pg
from ... import prepare as mp
from ... import tools as mt

import pygame
from .tilesV2 import *
from .decorations import *
from .player import Player

from ..level_select import *
from ..overworld_data import overworld_class as ovw


class Level:
    def __init__(self,level_data, surface):
        # GENERAL SETUP
        self.display_surface = surface
        self.world_shift = 0
        self.game_over = False
        self.reset = True

        #OVERWORL CONNECTION
        self.create_ovrwrld = Level_select()
        #self.current_level = ovw.current_level
        #self.level_data = levels
        #self.new_max_level = ovw_data['unlock']


        #TERRAIN SETUP
        terrain_layout = mt.import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        # GRASS SETUP
        grass_layout = mt.import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')

        # COINS
        coin_layout = mt.import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')
        self.coin_total = 0

        # JEWELS
        jewel_layout = mt.import_csv_layout(level_data['jewels'])
        self.jewel_sprite = self.create_tile_group(jewel_layout,'jewels')

        # CRATE
        crate_layout = mt.import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout,'crates')

        # FG PALMS
        fg_palm_layout = mt.import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        # BG PALMS
        bg_palm_layout = mt.import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(fg_palm_layout, 'bg palms')

        # SIGN
        sign_layout = mt.import_csv_layout(level_data['sign'])
        self.sign_sprite = self.create_tile_group(sign_layout, 'sign')

        # ENEMIES
        enemy_layout = mt.import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # CONSTRAINTS
        constraint_layout = mt.import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        #PLAYER SET UP
        player_layout = mt.import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)


        # DECORATIONS
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * mp.tile_size
        self.water = Water(mp.screen_height - 20, level_width)
        self.clouds = Clouds(400,level_width, 20)
        #----Coin UI ----
        self.coin_display = CoinDisplay()
        #----Lives UI----
        self.life = LivesDisplay()
        self.life_left = 5
        #----Jewels UI---
        self.ClueUI = GemClueDisplay()
        self.jewel_count = 0


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

                    if type == 'grass':
                        grass_tile_list = mt.import_cut_graphic('resources/graphics/level_graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(mp.tile_size,x,y,tile_surface)
                        sprite_group.add(sprite)

                    if type == 'crates':
                        sprite = Crate(mp.tile_size,x,y)
                        sprite_group.add(sprite)

                    if type == 'coins':
                        #sprite = Coin(tile_size,x,y,'../Graphics/coins')
                        # CODE TO CHANGE THE COLOR OF COINS
                        if val == '0':
                            sprite = Coin(mp.tile_size,x,y,'resources/graphics/level_graphics/coins/gold')
                            sprite_group.add(sprite)
                        if val == '1':
                            sprite = Coin(mp.tile_size,x,y,'resources/graphics/level_graphics/coins/silver')
                            sprite_group.add(sprite)

                    if type == 'fg palms':
                        if val == '0':
                            sprite = Palm(mp.tile_size, x, y, 'resources/graphics/level_graphics//terrain/palm_small')
                            sprite_group.add(sprite)
                        if val == '1':
                            sprite = Palm(mp.tile_size, x, y, 'resources/graphics/level_graphics//terrain/palm_large', 64)
                            sprite_group.add(sprite)

                    if type == 'bg palms':
                        sprite = Palm(mp.tile_size, x, y, 'resources/graphics/level_graphics//terrain/palm_bg', 64)
                        sprite_group.add(sprite)

                    if type == 'sign':
                        self.jewel_count = 0
                        sprite = Sign(mp.tile_size,x,y, self.jewel_count)
                        sprite_group.add(sprite)

                    if type == 'enemies':
                        sprite = mt.Enemy(mp.tile_size,x,y)
                        sprite_group.add(sprite)

                    if type == 'constraints':
                        sprite = Tile(mp.tile_size,x,y)
                        sprite_group.add(sprite)

                    if type == 'jewels':
                        sprite = Jewel(mp.tile_size,x,y,'resources/graphics/level_graphics/coins/jewels')
                        sprite_group.add(sprite)

        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()

    def enemy_speed(self):
        for enemy in self.enemy_sprites.sprites():
            if self.player.sprite.collision_rect.x - enemy.rect.x >= -400 and self.player.sprite.collision_rect.x - enemy.rect.x <= 400 and self.player.sprite.crouch != True and self.player.sprite.collision_rect.y - enemy.rect.y >= -20 and self.player.sprite.collision_rect.y - enemy.rect.y <= 20:
                if enemy.speed > 0:
                    enemy.speed = 7
                else:
                    enemy.speed = -7
            elif self.player.sprite.crouch == True:
                if enemy.speed > 0:
                    enemy.speed = 1
                else:
                    enemy.speed = -1
            else:
                if enemy.speed > 0:
                    enemy.speed = 1
                else:
                    enemy.speed = -1

    def horizontal_movement_collision(self):
        player = self.player.sprite

        player.collision_rect.x += player.direction.x * player.speed

        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x <0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0 :
                    player.collision_rect.right = sprite.rect.left
                    player.on_Right = True

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    #COIN/JEWEL COLLISION
    def coin_collection(self):
        player = self.player.sprite

        for coin in self.coin_sprites.sprites():
            if player.rect.colliderect(coin.rect):
                pygame.sprite.Sprite.remove(coin, self.coin_sprites)
                self.coin_total += 1

    def jewel_collision(self):
        player = self.player.sprite
        for jewel in self.jewel_sprite.sprites():
            if player.rect.colliderect(jewel.rect):
                pygame.sprite.Sprite.remove(jewel, self.jewel_sprite)
                self.jewel_count += 1

    def check_enemy_collisions(self):
        enemy_collisions = pg.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >+0:
                    self.player.sprite.direction.y = -15
                    enemy.kill()
                else:
                    if not self.player.sprite.invincible:
                        self.life_left -= 1
                        if self.life_left == 0:
                            self.game_over = True
                        self.player.sprite.invincible = True
                        self.hurt_time = pg.time.get_ticks()
    def check_invin(self):
        if self.player.sprite.invincible:
            current_time = pg.time.get_ticks()
            if current_time - self.hurt_time >= self.player.sprite.invincibility_duration:
                self.player.sprite.invincible = False

    def check_drown(self):
        # print(self.player.sprite.rect.bottom)
        # print(mp.screen_height)
        if self.player.sprite.rect.bottom >= (mp.screen_height + 128):
            self.game_over = True


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
                self.world_shift = -2
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

        # PARALLLAX BACKGROUND
        # LAYER 1
        # LAYER 2
        # LAYER 3
        # LAYER 4
        # Each layer is one level of the background, the smaller the layer number the father back the farther back the layer is. World shift is slower the smaller the number.

        # BG PALMS
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # TERRAIN
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # COINS
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        self.coin_display.draw(str(self.coin_total), self.display_surface)
        #print(self.coin_total)
        if self.jewel_count == 0:
            for sprite in self.sign_sprite.sprites():
                sprite.image.set_alpha(0)
                print(sprite.image.get_alpha())
        if self.jewel_count >= 3:
            for sprite in self.sign_sprite.sprites():
                sprite.image.set_alpha(255)
                print(sprite.image.get_alpha())

        self.jewel_sprite.update(self.world_shift)
        self.jewel_sprite.draw(self.display_surface)
        #print(self.coin_total)

        # LIVES
        self.life.draw(self.life_left, self.display_surface)

        # GRASS
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # ENEMIES
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_speed()
        self.enemy_sprites.draw(self.display_surface)

        # CHEST
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # SIGN
        self.sign_sprite.update(self.world_shift)
        self.sign_sprite.draw(self.display_surface)


        # FG PALMS
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)
        self.water.draw(self.display_surface, self.world_shift)

        # GEMS CLUE DISPLAY - extra comment
        self.ClueUI.draw(self.jewel_count, self.display_surface)
# =============== UNCOMMENT WHEN IMAGES ARE CREATED ==========================

        # PLAYER SPRITES
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.coin_collection()
        self.jewel_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)

        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_enemy_collisions()
        self.check_invin()
        self.check_drown()

        keys = pg.key.get_pressed()
        if keys[pg.K_j]:
            self.reset is not self.reset
        if keys[pg.K_o]:
            print(self.jewel_count)
        if keys[pg.K_p]:
            pass
        if self.player.sprite.CollBox == True:
            s = pg.Surface((self.player.sprite.collision_rect.width, self.player.sprite.collision_rect.height))
            s.set_alpha(100)
            s.fill((255,0,0))
            if self.player.sprite.CollBox1 == False:
                self.display_surface.blit(s, self.player.sprite.collision_rect )
            else:
                self.display_surface.blit(s, self.player.sprite.rect )
