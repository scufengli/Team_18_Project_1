import pygame
from Settings import *

class Maze:
    def __init__(self):
        self.M = 18
        self.N = 10

        self.bg_surf = pygame.image.load("Assets/background.png").convert()
        self.bg_surf = pygame.transform.scale(self.bg_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.block_surf = pygame.image.load("Assets/block.png").convert()
        self.block_surf = pygame.transform.scale(self.block_surf, (BLOCK_SIZE, BLOCK_SIZE))

        self.maze = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2,
                     1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,
                     1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
                     1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,
                     1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,
                     1,0,1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,
                     1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,
                     1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,
                     1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,0,]

    def update(self, display_surf):
        display_surf.blit(self.bg_surf, (0, 0))

        bx = 0
        by = 0

        for i in range(0, self.M * self.N):
            if self.maze[bx + (by * self.M)] == 1:
              display_surf.blit(self.block_surf, (bx * BLOCK_SIZE, by * BLOCK_SIZE))

            bx = bx + 1
            if bx > self.M-1:
                bx = 0
                by = by + 1