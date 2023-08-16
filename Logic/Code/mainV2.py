import pygame, sys
from settingsV2 import*
from levelV2 import Level
from game_data import level_0
from start_menuV2 import*
from supportV2 import*

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
menu = MainMenu(screen)

isMenu = True 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('grey')
    if isMenu == True:
        game_time = menu.run(event.type)
        if game_time:
            isMenu = False
    else:
        level.run()

    pygame.display.update()
    clock.tick(60)

