from Settings import *
from Entity import Entity
from SpriteStripAnim import SpriteStripAnim

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE

        self.right_frames = SpriteStripAnim('Swim_Right.png', (0, 0, 48, 48), 6, 1, True, ANIMATION_FRAMES)
        self.left_frames = SpriteStripAnim('Swim_Left.png', (0, 0, 48, 48), 6, 1, True, ANIMATION_FRAMES)
        self.frames = self.right_frames

    def can_move(self, maze, new_x, new_y):
        # Check if the player can move to the new position without colliding with walls
        for i in range(new_x // BLOCK_SIZE, (new_x + self.width) // BLOCK_SIZE + 1):
            for j in range(new_y // BLOCK_SIZE, (new_y + self.height) // BLOCK_SIZE + 1):
                if maze.maze[i + j * maze.M] == 1:
                    return False
        return True

    def moveRight(self, maze):
        self.frames = self.right_frames
        new_x = self.x + self.speed
        if new_x < (maze.M - 1) * BLOCK_SIZE and self.can_move(maze, new_x, self.y):
            self.x = new_x

    def moveLeft(self, maze):
        self.frames = self.left_frames
        new_x = self.x - self.speed
        if new_x >= 0 and self.can_move(maze, new_x, self.y):
            self.x = new_x

    def moveUp(self, maze):
        new_y = self.y - self.speed
        if new_y >= 0 and self.can_move(maze, self.x, new_y):
            self.y = new_y

    def moveDown(self, maze):
        new_y = self.y + self.speed
        if new_y < (maze.N - 1) * BLOCK_SIZE and self.can_move(maze, self.x, new_y):
            self.y = new_y

    def is_escaped(self, escape_point):
        return self.x + PLAYER_SIZE / 2 > escape_point.get_x_lower() and \
         self.x + PLAYER_SIZE / 2 < escape_point.get_x_upper() and \
          self.y + PLAYER_SIZE / 2 > escape_point.get_y_lower() and \
           self.y + PLAYER_SIZE / 2 < escape_point.get_y_upper()