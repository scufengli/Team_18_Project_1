from Settings import *

class Maze:
    def __init__(self):
        self.M = 18
        self.N = 10
        self.maze = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,
                     1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,
                     1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
                     1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,
                     1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,
                     1,0,1,0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,
                     1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,
                     1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,
                     1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                     1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,0,]

    def draw(self, displaySurface, imageSurface):
        bx = 0
        by = 0
        for i in range(0, self.M * self.N):
            if self.maze[bx + (by * self.M)] == 1:
                displaySurface.blit(imageSurface, (bx * BLOCK_SIZE, by * BLOCK_SIZE))

            bx = bx + 1
            if bx > self.M-1:
                bx = 0
                by = by + 1