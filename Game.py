import pygame
from pygame.locals import *
from Settings import *

from Player import Player
from Maze import Maze
from EscapePoint import EscapePoint
from AssetsLoader import AssetsLoader

class Game:
    clock = pygame.time.Clock()

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._player_surf = None
        self._bg_surf = None
        self._escape_surf = None
        self.start_time = pygame.time.get_ticks()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE)
        pygame.display.set_caption('The Cult of Barnacles')
        self._running = True

        asset_loader = AssetsLoader()
        asset_loader.load_animations()

        self.player = Player(asset_loader.animations['Player'])
        self.maze = Maze()
        self.escape_point = EscapePoint(asset_loader.animations['EscapePoint'], 1190, 0)
        self._bg_surf = pygame.image.load("Assets/background.png").convert()
        self._bg_surf = pygame.transform.scale(self._bg_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self._block_surf = pygame.image.load("Assets/block.png").convert()
        self._block_surf = pygame.transform.scale(self._block_surf, (BLOCK_SIZE, BLOCK_SIZE))

        self.ss_success = pygame.image.load("Assets/splash_pass.jpeg").convert()
        self.ss_success = pygame.transform.scale(self.ss_success, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.ss_failed = pygame.image.load("Assets/splash_fail.jpeg").convert()
        self.ss_failed = pygame.transform.scale(self.ss_failed, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self._player_surf = self.player.frames.next()
        self._escape_surf = self.escape_point.frames.next()
        self.clock.tick(FPS)

    def on_render(self):
        self._display_surf.blit(self._bg_surf, (0, 0))
        self._display_surf.blit(self._player_surf, (self.player.x, self.player.y))
        self.maze.draw(self._display_surf, self._block_surf)
        self.escape_point.draw(self._display_surf, self._escape_surf)
        pygame.display.flip()

    def on_win(self):
        self._display_surf.blit(self.ss_success, (0, 0))
        pygame.display.flip()

    def on_lose(self):
        self._display_surf.blit(self.ss_failed, (0, 0))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def get_seconds(self):
        return (pygame.time.get_ticks() - self.start_time) / 1000

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while True:
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
                self._running = False

            if self.get_seconds() > GAME_TIME:
                self.on_lose()
                self._running = False

            if self._running:
                self.on_loop()
                self.on_render()

        self.on_cleanup()