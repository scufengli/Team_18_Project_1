"""
The plash screen of the game is the first thing the user will see. 
"""

import pygame as pg
from ..import prepare as mp
from ..import tools as mt

class Splash(mt._State):
    """ This state is going to update while the game shows the splash screen."""
    def __init__(self):
        mt._State.__init__(self)
        self.next = "MAINMENU" #==== Note 1 ====#
        self.timeout = 5
        self.cover = pg.Surface((mp.screen_size)).convert_alpha()
        self.cover.fill(0)
        self.cover_alpha = 256
        self.alpha_step  = 2
        self.image = mp.GFX['Splash1']
        self.image = pg.transform.scale(self.image, mp.screen_size)
        self.rect = self.image.get_rect(center=mp.SCREEN_RECT.center)

    def update(self, surface, keys, current_time, time_delta):
        """Updates the splash screen."""
        self.current_time = current_time
        surface.blit(self.image,self.rect)
        self.cover.set_alpha(self.cover_alpha)
        self.cover_alpha = max(self.cover_alpha-self.alpha_step,0)
        surface.blit(self.cover,(0,0))
        if self.current_time-self.start_time > 1000.0*self.timeout:
            self.done = True

    def get_event(self, event):
        """ Keeps track of events. 
            Code that executes with events should go here. 
            EXAMPLES: KEY PRESSES AND MOUSE BUTTON
        """


"""
Note 1 : The name should match the exact spelling of the KEY in the states_dict.
The states_dict should be in the main.py, in the data folder.


"""