import pygame as pg
from ... import prepare as mp

class Player(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.frame_index = 0 
        self.animation_speed = 0.20
        self.animations = mp.AniDict
        self.image = self.animations['Idle'][self.frame_index]
        self.mask = pg.mask.from_surface(self.image)
        self.a,self.b,self.c,self.d = self.mask.get_bounding_rects()[0]
        rects = self.a,self.b,self.c,self.d
        print(rects)
        self.rect = self.image.get_rect( topleft = pos)

        # PLAYER MOVEMENT
        self.direction = pg.math.Vector2(0,0)
        self.speed = 0
        self.gravity = 0.8 
        self.jump_speed = -20
        self.collision_rect = pg.Rect(self.rect.topleft,(self.rect.width, self.rect.height))

        # PLAYER STATUS 
        self.status = 'Idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.crouch = False
        self.crouch_walk = False

    def animate(self):
        animation = self.animations[self.status]

    # LOOP OVER FRAME INDEX 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0 
        self.image = animation[int(self.frame_index)]
        self.image = pg.transform.scale_by(self.image, 1.5)
        self.rect = self.image.get_rect(x = self.rect.x, y = self.rect.y)

        # self.rect = self.image.get_rect(bottom = self.rect.bottom, width = self.bounding_rect[0][2], height = self.bounding_rect[0][3])

        if self.facing_right:
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pg.transform.flip(self.image,True,False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'Jump'
        elif self.direction.y > 1:
            self.status = 'Fall'
        else:
            if self.direction.x != 0:
                if self.crouch == False:
                    self.status = 'Run'
                elif self.crouch == True:
                    self.status = "Crouch_Walk"
            elif self.direction.x == 0: 
                if self.crouch == True:
                    self.status = "Crouch_Idle"
                else:
                    self.status ='Idle'

    def get_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pg.K_DOWN] and self.on_ground == True:
            self.crouch = True
        elif keys[pg.K_DOWN] and self.on_ground == True and (keys[pg.K_RIGHT]):
            self.crouch_walk = True
        elif keys[pg.K_DOWN] and self.on_ground == True and (keys[pg.K_LEFT]):
            self.crouch_walk = True
        else:
            self.direction.x = 0
            self.crouch, self.crouch_walk = False,False

        if keys[pg.K_SPACE] and self.on_ground:
            self.crouch, self.crouch_walk = False,False
            self.jump()
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += int(self.direction.y)

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self,):
        self.get_input()
        self.get_status()
        self.animate()