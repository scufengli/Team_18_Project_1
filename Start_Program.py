"""
This is the file that will start the game.


"""


import sys
import pygame as pg
from data.main import main # This line imports the main function from the data folder

if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()

def run():
    main()
    pg.quit()
    sys.exit()
