import pygame
from pygame.locals import *
from Settings import *

from Player import Player
from Maze import Maze
from EscapePoint import EscapePoint

class Game:
    clock = pygame.time.Clock()

    def __init__(self):
        self._running = True
        self._win = False
        self._display_surf = None
        self._image_surf = None
        self.bg_surf = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE)
        pygame.display.set_caption('The Cult of Barnacles')
        self._running = True
        self.player = Player()
        self.maze = Maze()
        self.escape_point = EscapePoint(70, 0)
        self._bg_surf = pygame.image.load("background.jpeg").convert()

        self.ss_success = pygame.image.load("SplashScreenPassed.jpeg").convert()
        self.ss_success = pygame.transform.scale(self.ss_success, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.ss_failed = pygame.image.load("SplashScreenFailed.jpeg").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self._image_surf = self.player.frames.next()
        self.clock.tick(FPS)

    def on_render(self):
        self._display_surf.blit(self._bg_surf, (0, 0))
        self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
        self.maze.draw(self._display_surf, self._bg_surf)
        pygame.display.flip()

    def on_win(self):
        self._display_surf.blit(self.ss_success, (0, 0))
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

            if self.player.is_escaped(self.escape_point):
                self.on_win()
                self._win = True

            if not self._win:
                self.on_loop()
                self.on_render()

        self.on_cleanup()