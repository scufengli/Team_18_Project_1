import pygame as pg
from .. import prepare as mp
from .. import tools as mt
from .overworld_data.overworld_class import Overworld
import sys

class Level_select(mt._State):
    def __init__(self,):
        mt._State.__init__(self)
        self.start_level = 0
        self.max_level = self.persist['max_level']
        # print('this is being ran')
        self.overworld = Overworld(self.start_level, self.max_level, self.persist)


        #MUSIC
        self.song = 'overworld'


    def startup(self, current_time, persistant):
        self.next = None
        self.done = False
        self.music_status = persistant['music_status']
        mt.Play_Music(self.music_status, self.song).Play_Pause()
        self.persist = persistant
        self.overworld = Overworld(self.start_level, self.max_level, self.persist)
        pass

    def cleanup(self):
        return mt._State.cleanup(self)

    def get_event(self, event):
        """EVENT CONTAINS ALL THE KEY PRESSES"""
        self.event = event
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN] or keys[pg.K_SPACE]:
            if self.persist['water_level_done'][self.persist['Current_level']] == False and self.persist["Current_level"] != 0:
                self.next = "WATERLEVEL"
                self.done = True
            else:
                self.persist["Current_level"] = self.overworld.current_level
                self.next = "GAMEPLAY"
                self.done = True

    def update(self, surface, keys, current_time, time_delta):
        """Update blink timer and draw everything."""
        self.overworld.run(self.persist)
        self.persist = self.overworld.persist
        self.current_time = current_time
