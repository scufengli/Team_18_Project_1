"""
The class for our Game scene is found here.
"""

import pygame as pg

from .. import prepare as mp # Module prepare
from .. import tools as mt # Module tools
from .Game1 import player

#========= TEST CODE ===========
#========= TEST CODE ===========


class Gameplay(mt._State):
    """This state could represent the actual gameplay phase."""
    def __init__(self):
        mt._State.__init__(self)
        # LEVEL SET UP
        self.display_surface = mp.SCREEN
        self.level_data = mp.level_map
        self.setup_level(self.level_data)
        self.blink = False
        self.timer = 0.0

        self.world_shift = 0 

        # PLAYER ATTRIBUTES
        self.clp = self.player.sprite



    def setup_level(self, layout):
        self.tiles = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index,cell in enumerate(row):
                x, y = col_index*mp.tile_size, row_index*mp.tile_size
                if cell == 'X':
                    tile = mt.Tile((x,y),mp.tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = player.Player((x,y))
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.clp
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < int(mp.screen_width/4) and direction_x < 0:
            self.world_shift = 8 
            player.speed = 0
        elif player_x > int(mp.screen_width*3/4) and direction_x > 0: 
            self.world_shift = -8
            player.speed = 0 
        else:
            self.world_shift = 0 
            player.speed = 8 

    def apply_gravity(self):
        player = self.clp
        player.direction.y += player.gravity
        player.rect.y += player.direction.y

    def horizontal_movement_collision(self):
        player = self.clp
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
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
        player = self.clp
        self.apply_gravity()

        for sprite in self.tiles.sprites():
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

    def jump(self):
        self.clp.direction.y = self.clp.jump_speed
        
    def animate(self):
        player = self.clp
        animation = player.animations[player.status]

        # LOOP OVER FRAME INDEX 
        player.frame_index += player.animation_speed
        if player.frame_index >= len(animation):
            player.frame_index = 0 

        image = animation[int(player.frame_index)]
        image = pg.transform.scale_by(image, 1.2)
        

        if player.facing_right:
            player.image = image


        else:
            flipped_image = pg.transform.flip(image,True,False)
            player.image = flipped_image



            
    def startup(self, current_time, persistant):
        """Load and play the music on scene start."""
        # pg.mixer.music.load(self.bgm)
        # pg.mixer.music.play(-1)
        # return mt._State.startup(self, current_time, persistant)

    def cleanup(self):
        """Stop the music when scene is done."""
        # pg.mixer.music.stop()
        return mt._State.cleanup(self)

    def get_event(self, event):
        """EVENT CONTAINS ALL THE KEY PRESSES"""
        player = self.clp
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            player.direction.x = 1
            player.facing_right = True
        elif keys[pg.K_LEFT]:
            player.direction.x = -1
            player.facing_right = False
        elif keys[pg.K_DOWN] and player.on_ground == True:
            player.crouch = True
        elif keys[pg.K_DOWN] and player.on_ground == True and (keys[pg.K_RIGHT] or keys[pg.K_LEFT]):
            player.crouch_walk = True

        else:
            player.direction.x = 0
            player.crouch, player.crouch_walk = False,False

        if keys[pg.K_SPACE] and player.on_ground:
            player.crouch, player.crouch_walk = False,False
            self.jump()

    def get_status(self):
        player = self.clp
        if player.direction.y < 0:
            player.status = 'Jump'
        elif player.direction.y > 1:
            player.status = 'Fall'
        else:
            if player.direction.x != 0:
                if player.crouch == False:
                    player.status = 'Run'
                elif player.crouch == True:
                    player.status = "Crouch_Walk"
            elif player.direction.x == 0: 
                if player.crouch == True:
                    player.status = "Crouch_Idle"
                else:
                    player.status ='Idle'

    def set_speed(self):
        player = self.clp
        if player.status == "Crouch_Walk":
            player.speed = 2
        else:
            player.speed = 8

    def draw(self, display_surface):
        """Blit all elements to surface."""
        player = self.clp
        display_surface.fill('black')
        # LEVEL TILES
        self.tiles.draw(self.display_surface)

        # PLAYER
        self.player.draw(self.display_surface)
        pg.draw.rect(self.display_surface, 'blue', self.clp.rect, width = 2)

        #===== TEST CODE =========

        #===== TEST CODE =========
        pass

    def update(self, surface, keys, current_time, time_delta):
        """Update blink timer and draw everything."""
        player = self.clp
        self.current_time = current_time
        if self.current_time-self.timer > 1000.0/5.0:
            self.blink = not self.blink
            self.timer = self.current_time

        self.tiles.update(self.world_shift)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.get_status()
        self.scroll_x()
        self.animate()
        # self.set_speed()
        self.draw(surface)
