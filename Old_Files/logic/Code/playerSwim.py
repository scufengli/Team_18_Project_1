import playerBase
import pygame

class PlayerSwim(playerBase.PlayerBase):
    def __init__(self, pos):
        super().__init__(pos)
        self.animations.update({'Swim': []})
        self.import_character_assets()
        self.animation_speed = 1
        self.facing_right = True

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_UP]:
            self.direction.y = 1
        elif keys[pygame.K_DOWN]:
            self.direction.y = -1
        else:
            self.direction.x = 0
            self.direction.y = 0

    def animate(self):
        animation = self.animations['Swim']

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

    def update(self):
        self.get_input()
        self.animate()