import pygame as pg
from .. import prepare as mp
from .. import tools as mt
import sys
from .Game1.level import Level
from .Game1.game_data import*

class Gameplay(mt._State):
    """This state could represent the actual gameplay phase."""
    def __init__(self):
        mt._State.__init__(self)
        self.level = Level(level_0, mp.SCREEN)

            
    def startup(self, current_time, persistant):
        """Load and play the music on scene start."""
        # pg.mixer.music.load(self.bgm)
        # pg.mixer.music.play(-1)
        # return mt._State.startup(self, current_time, persistant)

    def cleanup(self):
        """Stop the music when scene is done."""
        # pg.mixer.music.stop()
        return mt._State.cleanup(self)

    def get_event(self, event):
        """EVENT CONTAINS ALL THE KEY PRESSES"""
        self.event = event
        # player = self.clp
        # keys = pg.key.get_pressed()
        # if keys[pg.K_RIGHT]:
        #     player.direction.x = 1
        #     player.facing_right = True
        # elif keys[pg.K_LEFT]:
        #     player.direction.x = -1
        #     player.facing_right = False
        # elif keys[pg.K_DOWN] and player.on_ground == True:
        #     player.crouch = True
        # elif keys[pg.K_DOWN] and player.on_ground == True and (keys[pg.K_RIGHT] or keys[pg.K_LEFT]):
        #     player.crouch_walk = True

        # else:
        #     player.direction.x = 0
        #     player.crouch, player.crouch_walk = False,False

        # if keys[pg.K_SPACE] and player.on_ground:
        #     player.crouch, player.crouch_walk = False,False
        #     self.jump()
    def update(self, surface, keys, current_time, time_delta):
        """Update blink timer and draw everything."""
        self.level.run()
        self.current_time = current_time

