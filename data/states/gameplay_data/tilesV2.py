import pygame as pg
from ... import prepare as mp
from ... import tools as mt


class Tile(pg.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pg.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self,shift):
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface

class Crate(StaticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pg.image.load('resources/graphics/level_graphics/terrain/crate.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Sign(StaticTile):
    def __init__(self,size,x,y, jewel_count):
        super().__init__(size,x,y,pg.image.load('resources\graphics\level_graphics\wood_sign.png').convert_alpha())
        self.image = pg.transform.scale(self.image, (90,90))
        self.image = pg.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect(bottomleft = (x-20,y+120))
        self.image.set_alpha(0)


class AnimatedTile(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        self.size = size
        self.frames = mt.import_folder(path)
        self.frame_index = 0 
        if len(self.frames) >= 7:
            i = 0
            for frame in self.frames:
                self.frames[i] = pg.transform.scale(frame, (90,90))
                i += 1
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0 
        # self.image =  pg.transform.scale(self.frames[int(self.frame_index)], (64,64))
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift

class Coin(AnimatedTile):
    def __init__(self, size, x, y, path,):
        super().__init__(size, x, y, path)
        center_x = x + int(size/2)
        center_y = y + int(size/2)
        self.rect = self.image.get_rect(center = (center_x, center_y))


class Jewel(AnimatedTile):
    def __init__(self, size, x, y, path,):
        super().__init__(size, x, y, path)
        self.rect = self.image.get_rect(topleft = (x-20,y))
        self.rect.update((self.rect.topleft[0], self.rect.topleft[1]), (64, 64))


class Palm(AnimatedTile):
    def __init__(self, size,x,y,path, offset):
        super().__init__(size,x,y,path)
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)

