import pygame, sys
from setting import *
from tiles import Tile
from levelSwim import Level
from gameData import level_0
# PYGAME SETUP 

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

#========== TEST CODE ==========#


#========== END TEST CODE ==========#
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    bg = pygame.image.load('../Graphics/clouds.jpeg').convert()
    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)
