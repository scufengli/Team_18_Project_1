import pygame as pg
from .. import prepare as mp
from .. import tools as mt
from .overworld_data.overworld_class import Overworld
import sys

class Level_select(mt._State):
    def __init__(self,):
        mt._State.__init__(self)
        self.start_level = 1
        self.max_level = 4
        self.overworld = Overworld(self.start_level, self.max_level)

        
    def startup(self, current_time, persistant):
        pass

    def cleanup(self):

        return self.persist

    def get_event(self, event):
        """EVENT CONTAINS ALL THE KEY PRESSES"""
        self.event = event
        keys = pg.key.get_pressed()
        if keys[pg.K_KP_ENTER] or keys[pg.K_SPACE]:
            self.persist["Current_level"] = self.overworld.current_level
            print(self.persist['Current_level'])
            print(self.overworld.current_level)
            self.next = "GAMEPLAY"
            self.done = True

        
    def update(self, surface, keys, current_time, time_delta):
        """Update blink timer and draw everything."""
        self.overworld.run()
        self.current_time = current_time