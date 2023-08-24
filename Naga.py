from Settings import *
from Character import Character

class Naga(Character):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)

        self.counter = 0
        self.y_movement = 1
        self.state = 'move_left'
        self.center()

    def patrol(self):
        if self.counter % 120 == 0:
            self.y_movement *= -1
        
        if self.counter % 15 == 0:
            self.speed *= -1

        self.rect.y -= self.y_movement
        self.rect.x += self.speed
        self.counter += 1

    def update(self, display_surf):
        self.patrol()
        super().update(display_surf)