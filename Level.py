from Settings import *
from AssetsLoader import AssetsLoader

from Maze import Maze
from Fish import Fish
from Block import Block
from Bubble import Bubble
from Player import Player
from EscapePoint import EscapePoint

class Level:

    def __init__(self):
        self.entities = []
        self.blocks = []

        animation_loader = AssetsLoader()
        animation_loader.load_animations()
        self.animations = animation_loader.animations

        self.maze = Maze()
        self.register_entities()

    def register_entities(self):
        bx = 0
        by = 0

        for i in range(0, self.maze.M * self.maze.N):
            # print(bx * BLOCK_SIZE, by * BLOCK_SIZE, bx + (by * self.maze.M), self.maze.entities[bx + (by * self.maze.M)])
            match self.maze.entities[bx + (by * self.maze.M)]:
                case 1:
                    block = Block(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(block)
                    self.blocks.append(block)
                case 2:
                    self.player = Player(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(self.player)
                case 3:
                    self.escape_point = EscapePoint(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(self.escape_point)
                case 4:
                    self.register(Bubble(bx * BLOCK_SIZE, by * BLOCK_SIZE))
                case 5:
                    self.register(Fish(bx * BLOCK_SIZE, by * BLOCK_SIZE))

            bx += 1
            if bx > self.maze.M - 1:
                bx = 0
                by += 1

    def register(self, entity):
        entity.animation_setup(self.animations[entity.__class__.__name__])
        self.entities.append(entity)

    def escaped(self):
        return self.player.collide_rect(self.escape_point)

    def update(self, display_surf):
        for entity in self.entities:
            entity.update(display_surf)