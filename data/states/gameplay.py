import pygame as pg
from .. import prepare as mp
from .. import tools as mt
import sys
from .gameplay_data.game_data import level_dict
from ...Platformer.Code.level import Level

class Gameplay(mt._State):
    """This state could represent the actual gameplay phase."""
    def __init__(self,):
        mt._State.__init__(self) 
        self.level = Level(level_dict[str(self.persist['Current_level'])], mp.SCREEN)
            
    def startup(self, current_time, persistant):
        """Load and play the music on scene start."""
        # pg.mixer.music.load(self.bgm)
        # pg.mixer.music.play(-1)
        self.persist = persistant
        level_num = (str(self.persist['Current_level']))
        # print(level_dict[level_num])
        # print(type(level_dict[level_num]))
        # self.level = Level(level_dict[level_num], mp.SCREEN)
        return mt._State.startup(self, current_time, persistant)
        print('startup 1')

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
        print('running')
        if self.level.game_over == True:
            self.next = "LEVELSELECT" #REPLACE WITH GAME OVER SCREEN 
            print('done 3 ')
            self.level.game_over = False
            self.done = True
            

        
        self.current_time = current_time

