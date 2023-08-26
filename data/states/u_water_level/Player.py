from .Settings import*
from .Entity import*
from .SpriteStripAnim import*

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.speed = 25
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE

        self.lives_offset = 0
        self.freeze = False
        self.counter = 0
        self.armed = False
        self.hurt_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'player_hurt.mp3'))

    def is_player(self):
        return True
    def update(self, display_surf):
        super().update(display_surf)


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
