from Settings import *
from Entity import Entity
from SpriteStripAnim import SpriteStripAnim

class Character(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y, size = 48)
        self.speed = PLAYER_SPEED

        self.animations.update({'move_left': None, 'move_right': None})

    def can_move(self, level, new_x, new_y):
        for block in level.blocks:
            if (Entity(new_x, new_y, size = self.size).collide_rect(block)):
                return False
        return True

    def moveRight(self, level):
        self.state = 'move_right'
        new_x = self.rect.x + self.speed
        if self.can_move(level, new_x, self.rect.y):
            self.rect.x = new_x

    def moveLeft(self, level):
        self.state = 'move_left'
        new_x = self.rect.x - self.speed
        if self.can_move(level, new_x, self.rect.y):
            self.rect.x = new_x

    def moveUp(self, level):
        new_y = self.rect.y - self.speed
        if self.can_move(level, self.rect.x, new_y):
            self.rect.y = new_y

    def moveDown(self, level):
        new_y = self.rect.y + self.speed
        if self.can_move(level, self.rect.x, new_y):
            self.rect.y = new_y