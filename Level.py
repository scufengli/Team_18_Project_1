from Settings import *
from AssetsLoader import AssetsLoader

from Maze import Maze
from Fish import Fish
from Block import Block
from Bubble import Bubble
from Player import Player
from Naga import Naga
from Spear import Spear
from EscapePoint import EscapePoint

class Level:

    def __init__(self):
        animation_loader = AssetsLoader()
        animation_loader.load_animations()
        self.animations = animation_loader.animations

        self.reset(1)

    def reset(self, level):
        self.entities = []
        self.blocks = []
        self.enemies = []
        self.bubbles = []

        self.cur_level = level
        self.lives_left = PLAYER_LIVES

        self.maze = Maze()
        self.register_level(level)

    def register_level(self, level):
        entities = self.maze.get_maze(level)
        bx = 0
        by = 0

        for i in range(0, self.maze.M * self.maze.N):
            match entities[bx + (by * self.maze.M)]:
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
                    bubble = Bubble(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(bubble)
                    self.bubbles.append(bubble)
                case 5:
                    fish = Fish(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(fish)
                    self.enemies.append(fish)
                case 6:
                    naga = Naga(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(naga)
                    self.enemies.append(naga)
                case 7:
                    self.spear = Spear(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(self.spear)

            bx += 1
            if bx > self.maze.M - 1:
                bx = 0
                by += 1

    def register(self, entity):
        entity.animation_setup(self.animations[entity.__class__.__name__])
        self.entities.append(entity)

    def escaped(self):
        return self.player.collide_rect(self.escape_point)
    
    def remove_entity(self, entity):
        try:
            self.entities.remove(entity)
            self.bubbles.remove(entity)
            self.enemies.remove(entity)
        except ValueError:
            pass
        
    def update(self, display_surf):
        for entity in self.entities:
            entity.update(display_surf)
        
        for bubble in self.bubbles:
            if self.player.collide_rect(bubble):
                self.remove_entity(bubble)
                self.player.lives_offset += 2
        
        if self.player.collide_rect(self.spear):
            self.player.armed = True
            self.remove_entity(self.spear)

        if self.player.freeze is False:
            for enemy in self.enemies:
                if self.player.collide_rect(enemy):
                    if self.player.armed == True:
                        self.remove_entity(enemy)
                        self.player.armed = False
                    else:
                        self.player.lives_offset -= 1
                        self.player.freeze = True
        else:
            self.player.counter += 1
            if self.player.counter % 50 == 0:
                self.player.freeze = False

    def next(self):
        self.reset(self.cur_level + 1)
