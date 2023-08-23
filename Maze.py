import pygame
from Settings import *

class Maze:
    def __init__(self):
        self.M = 18
        self.N = 10

        self.entities = [
            2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,3,
            1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,
            1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
            1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,
            1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,
            1,0,1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,
            1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,0,
        ]