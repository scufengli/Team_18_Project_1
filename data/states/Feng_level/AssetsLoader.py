import os
from .Settings import *
from .SpriteStripAnim import SpriteStripAnim

class AssetsLoader:
    def __init__(self):
        self.animations = {}

    def load_animations(self):
        path = os.path.join(ROOT_PATH, ANIMATION_PATH)
        entity_dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

        for entity in entity_dirs:
            for filename in os.listdir(os.path.join(path, entity)):
                if not filename.startswith('.'):
                    num_frames = int(filename.split('-')[0])
                    sprite_size = int(filename.split('-')[1])
                    state = filename.split('-')[2].split('.')[0]

                    entity_animations = self.animations.setdefault(entity, {})
                    entity_animations[state] = SpriteStripAnim(os.path.join(path, entity, filename), (0, 0, sprite_size, sprite_size), num_frames, -1, True, ANIMATION_FRAMES)

