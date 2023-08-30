from .Settings import *
from .Entity import Entity

class Character(Entity):
    def __init__(self, x = 0, y = 0, size = 48):
        super().__init__(x, y, size)
        # refer to Settings.py
        self.speed = PLAYER_SPEED

        self.animations.update({'move_left': None, 'move_right': None})
        self.center()

    def can_move(self, level, new_x, new_y):
        for block in level.blocks:
            if (Entity(new_x, new_y, size = self.size).collide_rect(block)):
                return False
        return new_x >= -10 and new_x <= CAMERA_WIDTH + 10 and new_y >= -10 and new_y <= CAMERA_HEIGHT + 10

    def move_right(self, level):
        self.state = 'move_right'
        new_x = self.rect.x + self.speed
        if self.can_move(level, new_x, self.rect.y):
            self.rect.x = new_x
            return True
        return False

    def move_left(self, level):
        self.state = 'move_left'
        new_x = self.rect.x - self.speed
        if self.can_move(level, new_x, self.rect.y):
            self.rect.x = new_x
            return True
        return False

    def move_up(self, level):
        new_y = self.rect.y - self.speed
        if self.can_move(level, self.rect.x, new_y):
            self.rect.y = new_y
            return True
        return False

    def move_down(self, level):
        new_y = self.rect.y + self.speed
        if self.can_move(level, self.rect.x, new_y):
            self.rect.y = new_y
            return True
        return False