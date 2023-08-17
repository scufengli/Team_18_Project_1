class Entity:
    def __init__(self, animations):
        self.x = 0
        self.y = 0

        self.frames = None
        self.animations = {'idle': None}
        self.state = 'idle'

        self.animation_setup(animations)
        self.frames = self.animations['idle']

    def animation_setup(self, _animations):
        for state in self.animations.keys():
            self.animations[state] = _animations[state]