import pygame
from pygame.locals import *

import spritesheet
# https://www.pygame.org/wiki/Spritesheet
from sprite_strip_anim import SpriteStripAnim



class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 2
        self.width = 48
        self.height = 48

        self.frames = SpriteStripAnim('Swim.png', (0, 0, 48, 48), 6, 1, True, 5)

    def can_move(self, maze, new_x, new_y):
        # Check if the player can move to the new position without colliding with walls
        for i in range(new_x // 70, (new_x + self.width) // 70 + 1):
            for j in range(new_y // 70, (new_y + self.height) // 70 + 1):
                if maze.maze[i + j * maze.M] == 1:
                    return False
        return True

    def moveRight(self, maze):
        new_x = self.x + self.speed
        if new_x < (maze.M - 1) * 70 and self.can_move(maze, new_x, self.y):
            self.x = new_x

    def moveLeft(self, maze):
        new_x = self.x - self.speed
        if new_x >= 0 and self.can_move(maze, new_x, self.y):
            self.x = new_x

    def moveUp(self, maze):
        new_y = self.y - self.speed
        if new_y >= 0 and self.can_move(maze, self.x, new_y):
            self.y = new_y

    def moveDown(self, maze):
        new_y = self.y + self.speed
        if new_y < (maze.N - 1) * 70 and self.can_move(maze, self.x, new_y):
            self.y = new_y


class Maze:
    def __init__(self):
        self.M = 18
        self.N = 10
        self.maze = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                     1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,
                     1,0,1,0,0,0,0,0,0,1,0,1,1,1,1,1,0,1,
                     1,0,1,0,1,1,1,1,0,1,0,1,1,1,1,1,0,1,
                     1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,
                     1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,]

    def draw(self, display_surf, image_surf):
        bx = 0
        by = 0
        for i in range(0, self.M * self.N):
            if self.maze[bx + (by * self.M)] == 1:
                display_surf.blit(image_surf, (bx * 70, by * 70))

            bx = bx + 1
            if bx > self.M-1:
                bx = 0 
                by = by + 1


class App:
    windowWidth = 1260
    windowHeight = 700
    clock = pygame.time.Clock()

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self.player = Player()
        self.maze = Maze()
        '''
        self._image_surf = pygame.image.load("player.png").convert()
        self._image_surf = pygame.transform.scale(self._image_surf, (48, 48))
        '''
        self._block_surf = pygame.image.load("block.png").convert()
        self._block_surf = pygame.transform.scale(self._block_surf, (70, 70))

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self._image_surf = self.player.frames.next()
        self.clock.tick(60)

    def is_escaped(self):
        if self.player.x > 70 and self.player.x < 140 and self.player.y > 70 and self.player.y < 140:
            return True
        return False

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
        self.maze.draw(self._display_surf, self._block_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.player.moveRight(self.maze)

            if keys[K_LEFT]:
                self.player.moveLeft(self.maze)

            if keys[K_UP]:
                self.player.moveUp(self.maze)

            if keys[K_DOWN]:
                self.player.moveDown(self.maze)

            if keys[K_ESCAPE]:
                self._running = False

            if self.is_escaped():
                break


        

            self.on_loop()
            self.on_render()

        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
