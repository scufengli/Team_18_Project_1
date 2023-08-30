"""
This module contains the fundamental Control class and a prototype class
for States.  Also contained here are resource loading functions.
"""

import os
import pygame as pg
from . import prepare as mp #==== Note 1 ====#
from csv import reader
from os import walk
from random import randint
from .states.gameplay_data.tilesV2 import AnimatedTile

### CLASSES
class Control(object):
    """Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here."""
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.show_fps = True
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        """Given a dictionary of States and a State to start in,
        builds the self.state_dict."""
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self,dt):
        """Checks if a state is done or has called for a game quit.
        State is flipped if neccessary and State.update is called."""
        self.current_time = pg.time.get_ticks()
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()

#================================================

        self.state.update(self.screen, self.keys, self.current_time, dt)
# RUNS THE UPDATE METHOD WITHIN THE STATE MODULE

# wHEN SELF.DONE IS EQUAL TO TRUE IT WILL THEN THE THE FLIP_STATE CONTROL CLASS METHOD THAT CHANGES THE CURRENT STATE.

# AFTER THE STATE CHANGE THE UPDATE METHOD OF THE NEXT STATE WILL RUN.
#================================================
    def flip_state(self):
        """When a State changes to done necessary startup and cleanup functions
        are called and the current State is changed."""
        previous,self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)
        self.state.previous = previous

    def event_loop(self):
        """Process all events and pass them down to current State.  The f5 key
        globally turns on/off the display of FPS in the caption"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.state.get_event(event)

    def toggle_show_fps(self, key):
        """Press f5 to turn on/off displaying the framerate in the caption."""
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)

    def main(self):
        """Main loop for entire program."""
        while not self.done:
            time_delta = self.clock.tick(self.fps)/1000.0
            self.event_loop()

#================================================

            self.update(time_delta)
# RUNS THE UPDATE METHOD IN THE CONTROL CLASS
# LINE 34
#================================================
            pg.display.update()
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
                pg.display.set_caption(with_fps)

class _State(object):
    """This is a prototype class for States.  All states should inherit from it.
    No direct instances of this class should be created. get_event and update
    must be overloaded in the childclass.  startup and cleanup need to be
    overloaded when there is data that must persist between States."""
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None


# ========== Inventory Items are going to be placed within the self.persist variable. ==========

        self.persist = {"Current_level": 0, 'max_level': 4, 'water_level_done': [False,False,False]}

# ========== Inventory Items are going to be placed within the self.persist variable. ==========

    def get_event(self, event):
        """Processes events that were passed from the main event loop.
        Must be overloaded in children."""
        pass

    def startup(self, current_time, persistant):
        """Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time."""
        self.persist = persistant
        self.start_time = current_time

    def cleanup(self):
        """Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False."""
        self.done = False
        return self.persist

    def update(self, surface, keys, current_time):
        """Update function for state.  Must be overloaded in children."""
        pass

    def render_font(self, font, msg, color, center):
        """Returns the rendered font surface and its rect centered on center."""
        msg = font.render(msg, 1, color)
        rect = msg.get_rect(center=center)
        return msg, rect

class Button():
    def __init__(self,pos,text_input,font,size, base_color,hovering_color,display_surface, image):
        self.image = image
        self.x_pos, self.y_pos = pos[0],pos[1]
        if self.image is None:
            self.font = pg.font.Font(font, size)
            self.base_color, self.hovering_color = base_color, hovering_color
            self.text_input = text_input
            self.text = self.font.render(self.text_input,True,self.base_color)
            self.image = self.text
            self.text_rect = self.text.get_rect(topleft =(self.x_pos, self.y_pos))
        self.rect = self.image.get_rect(topleft =(self.x_pos, self.y_pos))

    def update(self,display_surface):
        if self.image is None:
            display_surface.blit(self.text,self.text_rect)
        else:
            display_surface.blit(self.image, self.rect)

    def check_for_input(self,position):
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)

    def change_color(self,position):

        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.tect = self.font.render(self.text_input,True,self.hovering_color)
        else:
            self.tect = self.font.render(self.text_input,True,self.base_color)

class ImgBtn():
    def __init__(self, image, pos, rect, display):
        x, y = pos
        self.rect = rect
        display.blit(image, image.get_rect(center = self.rect.center))

    def check_clicked(self, position):
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)


class Enemy(AnimatedTile):
	def __init__(self,size,x,y):
		super().__init__(size,x,y,'resources/graphics/level_graphics/enemy/run')
		self.rect.y += size - (self.image.get_size()[1])+10
		self.speed = randint(1,2)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pg.transform.flip(self.image,True,False)

	def reverse(self):
		self.speed *= -1

	def update(self,shift):
		self.rect.x += shift
		self.animate()
		self.move()
		self.reverse_image()

### Resource loading functions.
def load_all_gfx(directory,colorkey=(255,0,255),accept=(".png",".jpg",".bmp")):
    """Load all graphics with extensions in the accept argument.  If alpha
    transparency is found in the image the image will be converted using
    convert_alpha().  If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey."""
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics

def load_all_music(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """Create a dictionary of paths to music files in given directory
    if their extensions are in accept."""
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs

def load_all_fonts(directory, accept=(".ttf",)):
    """Create a dictionary of paths to font files in given directory
    if their extensions are in accept."""
    return load_all_music(directory, accept)

def load_all_movies(directory, accept=(".mpg",)):
    """Create a dictionary of paths to movie files in given directory
    if their extensions are in accept."""
    return load_all_music(directory, accept)

def load_all_sfx(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """Load all sfx of extensions found in accept.  Unfortunately it is
    common to need to set sfx volume on a one-by-one basis.  This must be done
    manually if necessary in the setup module."""
    effects = {}
    for fx in os.listdir(directory):
        name,ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects

def load_animations_from_folders(character):
    AnimationsDict = {}
    folders = os.listdir(os.path.join("resources", "graphics",character))
    for folder in folders:
        CharAnimations = []
        for image in os.listdir(os.path.join("resources", "graphics","character", folder)):
            path = f'./resources/graphics/character/{folder}/{image}'
            image_surf = pg.image.load(path)
            image_surf = pg.transform.scale_by(image_surf, 1.5)
            CharAnimations.append(image_surf)
        AnimationsDict[folder] = CharAnimations
    return AnimationsDict

def strip_from_sheet(sheet, start, size, columns, rows=1):
    """Strips individual frames from a sprite sheet given a start location,
    sprite size, and number of columns and rows."""
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames

def strip_coords_from_sheet(sheet, coords, size):
    """Strip specific coordinates from a sprite sheet."""
    frames = []
    for coord in coords:
        location = (coord[0]*size[0], coord[1]*size[1])
        frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames

def get_cell_coordinates(rect, point, size):
    """Find the cell of size, within rect, that point occupies."""
    cell = [None, None]
    point = (point[0]-rect.x, point[1]-rect.y)
    cell[0] = (point[0]//size[0])*size[0]
    cell[1] = (point[1]//size[1])*size[1]
    return tuple(cell)

def cursor_from_image(image):
    """Take a valid image and create a mouse cursor."""
    colors = {(0,0,0,255) : "X",
              (255,255,255,255) : "."}
    rect = image.get_rect()
    icon_string = []
    for j in range(rect.height):
        this_row = []
        for i in range(rect.width):
            pixel = tuple(image.get_at((i,j)))
            this_row.append(colors.get(pixel, " "))
        icon_string.append("".join(this_row))
    return icon_string

### IMPORT FUNCTIONS
def import_folder(path):
	surface_list = []

	for _,__,image_files in walk(path):
		for image in image_files:
			full_path = path + '/' + image
			image_surf = pg.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphic(path):
    surface = pg.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / mp.tile_size)
    tile_num_y = int(surface.get_size()[1] / mp.tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x, y = col * mp.tile_size, row * mp.tile_size
            new_surf = pg.Surface((mp.tile_size, mp.tile_size), flags= pg.SRCALPHA)
            new_surf.blit(surface, (0,0), pg.Rect(x,y,mp.tile_size, mp.tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles

def import_character_assets():
    character_path = '../resources/graphics/character/'
    animations = {'Idle':[],'Run':[],'Crouch_Idle':[],'Crouch_Walk':[],'Hurt':[],'Jump':[],'Land':[],'Death':[], 'Fall':[]}

    for animation in animations.keys():
        full_path = character_path + animation
        animations[animation] = import_folder(full_path)


    return animations

### DRAW FUNCTIONS
def draw_text( text, font_type, size, x, y, color, display_surface):
    font = pg.font.Font(font_type, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    display_surface.blit(text_surface, text_rect)

def draw_newline_text(text, font_type, size, space, pos, color, surface):
    paragraph = []
    font = pg.font.Font(font_type, size)
    for line in text:
        paragraph.append(font.render(line, True, color))

    for line in range(len(paragraph)):
        surface.blit(paragraph[line],(pos[0],pos[1]+(line*size)+(space*line)))
