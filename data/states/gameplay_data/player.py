import pygame as pg
from ... import prepare as mp

class Player(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.frame_index = 0 
        self.animation_speed = 0.20
        self.animations = mp.AniDict
        self.image = self.animations['Idle'][self.frame_index]
        self.pos = pos


        self.CollBox = True
        self.CollBox1 = False


        # PLAYER MOVEMENT
        self.direction = pg.math.Vector2(0,0)
        self.speed = 0
        self.gravity = 0.8 
        self.jump_speed = -20
        self.rect = self.image.get_rect(topleft = pos)
        self.x_offset = 24
        self.y_offset = 12
        # self.mask = pg.mask.from_surface(self.image)
        # self.a,self.b,self.c,self.d = self.mask.get_bounding_rects()[0]
        # rects = self.a,self.b,self.c,self.d
        # print(rects)

        # x,y,w,h = self.rect = self.image.get_bounding_rect()
        x,y,w,h = self.image.get_bounding_rect()
        self.x, self.y = x, y
        self.h = h 
        # self.collision_rect = pg.Rect((self.rect.x, self.rect.y),(w, h))
        # self.collision_rect = pg.Rect((pos[0]+20, pos[1]+20),(w,h+20))
        self.collision_rect = pg.Rect((self.rect.x, self.rect.y),(w, h))
        

        # self.collision_rect = self.image.get_clip()
        # self.collision_rect = pg.Rect((pos[0], pos[1]),(w, h))



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
        # self.rect.top = self.collision_rect.top
    # LOOP OVER FRAME INDEX 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0 
        self.image = animation[int(self.frame_index)]

        # self.rect.bottomright = self.collision_rect.bottomright
        # self.rect.update(self.collision_rect)

        if self.facing_right:
            self.rect.right = self.collision_rect.right + self.x_offset
            self.rect.bottom = self.collision_rect.bottom + 15
            if self.crouch:
                self.collision_rect.height, self.collision_rect.bottom = self.h - 20, self.collision_rect.bottom - self.y_offset + 12
            if self.crouch == False:
                self.collision_rect.height, self.collision_rect.bottom = self.h, self.collision_rect.bottom - self.y_offset + 12
        else:
            flipped_image = pg.transform.flip(self.image,True,False)
            self.image = flipped_image
            if self.crouch:
                self.collision_rect.height, self.collision_rect.bottom = self.h - 20, self.collision_rect.bottom - self.y_offset + 12
            if self.crouch == False:
                self.collision_rect.height, self.collision_rect.bottom = self.h, self.collision_rect.bottom - self.y_offset + 12
            self.rect.right = self.collision_rect.right + self.x_offset
            self.rect.bottom = self.collision_rect.bottom + 15


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


        elif keys[pg.K_g]:
            self.CollBox = not self.CollBox
        elif keys[pg.K_h]:
            self.CollBox1 = not self.CollBox1


        elif keys[pg.K_DOWN] and self.on_ground == True:
            self.crouch = True
            self.direction.x = 0
            self.crouch_walk = False
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