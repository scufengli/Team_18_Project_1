import sys, os
import pygame
from Settings import *
from pygame.locals import *

from Level import Level
from HealthBar import HealthBar

class Game:
    clock = pygame.time.Clock()

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self._running = True
        self.display_surf = None
        self.level = None
        self.start_time = pygame.time.get_ticks()
        self.max_level = 2

    def on_init(self):
        self.display_surf = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('The Cult of Barnacles')
        pygame.mixer.music.load(os.path.join(ROOT_PATH, SOUND_PATH, 'bg_music.mp3'))
        pygame.mixer.music.play(1, 0.0)

        self.level = Level()
        self.healthbar = HealthBar()

        self.ss_success = pygame.image.load(os.path.join(ROOT_PATH, 'splash_pass.png')).convert()
        self.ss_success = pygame.transform.scale(self.ss_success, (CAMERA_WIDTH, CAMERA_HEIGHT))

        self.ss_failed = pygame.image.load(os.path.join(ROOT_PATH, 'splash_fail.png')).convert()
        self.ss_failed = pygame.transform.scale(self.ss_failed, (CAMERA_WIDTH, CAMERA_HEIGHT))

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.clock.tick(FPS)

    def on_render(self):
        self.level.lives_left = int((GAME_TIME - self.get_seconds()) / GAME_TIME * 6) + self.level.player.lives_offset
        self.bg_surf = pygame.image.load(os.path.join(ROOT_PATH, 'background.png')).convert()
        self.bg_surf = pygame.transform.scale(self.bg_surf, (CAMERA_WIDTH, CAMERA_HEIGHT))
        self.display_surf.blit(self.bg_surf, (0, 0))

        self.level.update(self.display_surf)
        self.healthbar.draw(self.level.lives_left, self.display_surf)

        pygame.display.update()


    def on_win(self):
        self.display_surf.blit(self.ss_success, (0, 0))
        pygame.display.update()
        if self.level.cur_level == self.max_level:
            self._running = False
        else:
            pygame.time.wait(3000)
            self.level.next()

    def on_lose(self):
        self.display_surf.blit(self.ss_failed, (0, 0))
        pygame.display.update()

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
                self.level.player.move_right(self.level)

            if keys[K_LEFT]:
                self.level.player.move_left(self.level)

            if keys[K_UP]:
                self.level.player.move_up(self.level)

            if keys[K_DOWN]:
                self.level.player.move_down(self.level)

            if keys[K_ESCAPE]:
                pygame.quit()
                sys.exit()

            if self.level.escaped() and self.level.lives_left > 0:
                self.on_win()
                
            if self.level.lives_left == 0:
                self.on_lose()
                self._running = False

            if self._running:
                self.on_loop()
                self.on_render()
