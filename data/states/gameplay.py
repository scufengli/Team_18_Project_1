import pygame as pg
from .. import prepare as mp
from .. import tools as mt
import sys
from .gameplay_data.level import Level
from .gameplay_data.game_data import*

class Gameplay(mt._State):
    """This state could represent the actual gameplay phase."""
    def __init__(self,):
        mt._State.__init__(self) 
        self.level = Level(level_dict['0'], mp.SCREEN)


            
    def startup(self, current_time, persistant):
        """Load and play the music on scene start."""
        # pg.mixer.music.load(self.bgm)
        # pg.mixer.music.play(-1)
        self.persist = persistant
        level_num = (str(self.persist['Current_level']))
        print(type(level_dict[level_num]))
        print(level_dict[level_num])
        self.level = Level(level_dict[level_num], mp.SCREEN)
        # return mt._State.startup(self, current_time, persistant)

    def cleanup(self):
        """Stop the music when scene is done."""
        # pg.mixer.music.stop()
        return mt._State.cleanup(self)

    def get_event(self, event):
        """EVENT CONTAINS ALL THE KEY PRESSES"""
        self.event = event
        
    def update(self, surface, keys, current_time, time_delta):
        """Update blink timer and draw everything."""
        self.level.run()
        self.current_time = current_time

