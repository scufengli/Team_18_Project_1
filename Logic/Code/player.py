import pygame
from support import import_folder
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0 
        self.animation_speed = 0.20
        self.image = self.animations['Idle'][self.frame_index]

        # ===== TEMP PLAYER PLACE HOLDER =====
        # self.image = pygame.Surface((32,64))
        # self.image.fill('red')
        # ===== END =====
        self.rect = self.image.get_rect(topleft = pos)
        self.rect = pygame.Rect(pos[0], pos[1], 64, 44)


        

        # PLAYER MOVEMENT 
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -20

        # PLAYER STATUS
        self.status = 'Idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.crouch = False
        self.crouch_walk = False

    def import_character_assets(self):
        character_path = '../Graphics/Character/'
        self.animations = {'Idle':[],'Run':[],'Crouch_Idle':[],'Crouch_Walk':[],'Hurt':[],'Jump':[],'Land':[],'Death':[], 'Fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # LOOP OVER FRAME INDEX 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0 

        image = animation[int(self.frame_index)]
        image = pygame.transform.scale_by(image, 1.5)
        

        if self.facing_right:
            self.image = image
            # pygame.draw.rect(self.image, (255,0,0), [0, 0, self.rect[2], self.rect[3]], 1)
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
            # pygame.draw.rect(self.image, (255,0,0), [0, 0, self.rect[2], self.rect[3]], 1)

        # SET THE RECT 
        rx,ry,rw,rh = self.rect
        rw, rh = 64, 59
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
            self.rect = pygame.Rect(rx,ry,rw,rh)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            self.rect = pygame.Rect(rx,ry,rw,rh)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.rect = pygame.Rect(rx,ry,rw,rh)            
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
            self.rect = pygame.Rect(rx,ry,rw,rh)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
            self.rect = pygame.Rect(rx,ry,rw,rh)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
            self.rect = pygame.Rect(rx,ry,rw,rh)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)
            self.rect = pygame.Rect(rx,ry,rw,rh)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_DOWN] and self.on_ground == True:
            self.crouch = True
        elif keys[pygame.K_DOWN] and self.on_ground == True and (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            self.crouch_walk = True
        elif keys[pygame.K_UP] and self.on_ground == True:
            self.crouch = False
            
        else:
            self.direction.x = 0
            self.crouch, self.crouch_walk = False,False

        if keys[pygame.K_SPACE] and self.on_ground:
            self.crouch, self.crouch_walk = False,False
            self.jump()

    # def get_status(self):
    #     if self.direction.y < 0:
    #         self.status = 'Jump'
    #     elif self.direction.y > 1:
    #         self.status = 'Fall'
    #     else:
    #         if self.direction.x != 0 and self.crouch == False:
    #             self.speed = 8
    #             self.status = 'Run'
    #         elif self.direction.x == 0 and self.crouch == True:
    #             self.status = "Crouch_Idle"
    #         elif self.direction.x != 0 and self.crouch == True:
    #             self.speed = 2
    #             self.status = "Crouch_Walk"
    #         else:
    #             self.status ='Idle'
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'Jump'
        elif self.direction.y > 1:
            self.status = 'Fall'
        else:
            if self.direction.x != 0:
                if self.crouch == False:
                    # self.speed = 8
                    self.status = 'Run'
                elif self.crouch == True:
                    self.speed = 2
                    self.status = "Crouch_Walk"
            elif self.direction.x == 0: 
                if self.crouch == True:
                    self.status = "Crouch_Idle"
                else:
                    self.status ='Idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += int(self.direction.y)

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
