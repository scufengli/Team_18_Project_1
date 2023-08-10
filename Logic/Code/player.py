import pygame
import playerBase

class Player(playerBase.PlayerBase):
    def __init__(self, pos):
        super().__init__(pos)
        self.animations.update({'Idle':[],'Run':[],'Crouch_Idle':[],'Crouch_Walk':[],'Hurt':[],'Jump':[],'Land':[],'Death':[], 'Fall':[]})
        self.import_character_assets()
        self.animation_speed = 0.20
        self.image = self.animations['Idle'][self.frame_index]

        # ===== TEMP PLAYER PLACE HOLDER =====
        # self.image = pygame.Surface((32,64))
        # self.image.fill('red')
        # ===== END =====

        # PLAYER MOVEMENT 
        self.gravity = 0.8
        self.jump_speed = -16

        # PLAYER STATUS
        self.status = 'Idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def animate(self):
        animation = self.animations[self.status]

        # LOOP OVER FRAME INDEX
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0 

        image = animation[int(self.frame_index)]

        if self.facing_right:
            self.image = image
            pygame.draw.rect(self.image, (255,0,0), [0, 0, self.rect[2], self.rect[3]], 1)
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
            pygame.draw.rect(self.image, (255,0,0), [0, 0, self.rect[2], self.rect[3]], 1)

        # SET THE RECT
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'Jump'
        elif self.direction.y > 1:
            self.status = 'Fall'
        else:
            if self.direction.x != 0:
                self.status = 'Run'
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
