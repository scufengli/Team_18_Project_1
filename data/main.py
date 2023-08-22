"""
The main function starts here.
It will create an instance of 'Game Controller'.
It will add the game states to a dictionary called state_dict by using tools.setup_states.
THERE IS NO NEED TO EDIT 'tools.Control' class.

ALL MODIFICATIONS SHOULD OCCUR IN THIS MODULE, AND IN THE PREPARE MODULE.

"""


from . import prepare, tools 
from .states import gameplay, level_select, splash, main_menu #==== Note 1 ====#

def main():
    """Add states to control here."""
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {"SPLASH" : splash.Splash(),
                  "MAINMENU" : main_menu.Main_Menu(),
                  "GAMEPLAY" : gameplay.Gameplay(),
                  "LEVELSELECT" : level_select.Level_select()
                  #"STATE NAME" . <State Module Name>.<State Class()>
                  }
#======== TEMP CODE =========
    run_it.setup_states(state_dict, "LEVELSELECT")
    run_it.main()
#======== TEMP CODE =========
# #======== DONT DELETE =========
#     run_it.setup_states(state_dict, "SPLASH")
#     run_it.main()
# #======== DONT DELETE =========


"""
Note 1: Make sure to properly name the KEYS in the state_dict.
"""
