import sys
import pygame
from pygame.locals import *
from Settings import *

from Player import Player
from Maze import Maze
from EscapePoint import EscapePoint
from Bubble import Bubble
from Fish import Fish
from AssetsLoader import AssetsLoader

class Game:
    clock = pygame.time.Clock()

    def __init__(self):
        pygame.init()
        self._running = True
        self.display_surf = None
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.SysFont("Times New Roman", 20, True)

    def on_init(self):
        self.display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE)
        pygame.display.set_caption('The Cult of Barnacles')

        asset_loader = AssetsLoader()
        asset_loader.load_animations()

        self.player = Player(asset_loader.animations['Player'])
        self.maze = Maze()
        self.escape_point = EscapePoint(asset_loader.animations['EscapePoint'], 1190, 0)
        self.bubble = Bubble(asset_loader.animations['Bubble'], 70, 0)
        self.fish = Fish(asset_loader.animations['Fish'], 280, 0)

        self.ss_success = pygame.image.load("Assets/splash_pass.png").convert()
        self.ss_success = pygame.transform.scale(self.ss_success, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.ss_failed = pygame.image.load("Assets/splash_fail.jpeg").convert()
        self.ss_failed = pygame.transform.scale(self.ss_failed, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.clock.tick(FPS)

    def on_render(self):
        self.maze.update(self.display_surf)
        self.escape_point.update(self.display_surf)
        self.bubble.update(self.display_surf)
        self.player.update(self.display_surf)
        self.fish.update(self.display_surf)
        self.display_surf.blit(self.font.render("Oxygen Level: " + str(round((GAME_TIME - self.get_seconds()) / GAME_TIME * 100, 2)) + "%", 1, (255, 255, 255)), (10, 675))

    def on_win(self):
        self.display_surf.blit(self.ss_success, (0, 0))

    def on_lose(self):
        self.display_surf.blit(self.ss_failed, (0, 0))

    def on_cleanup(self):
        pygame.quit()

    def get_seconds(self):
        return (pygame.time.get_ticks() - self.start_time) / 1000

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while True:
            for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()

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

            pygame.display.flip()


        self.on_cleanup()