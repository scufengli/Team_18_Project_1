import os, pygame, sys
BLOCK_SIZE = 70
PLAYER_SIZE = 48
PLAYER_SPEED = 6
PLAYER_LIVES = 5

CAMERA_WIDTH = 1260
CAMERA_HEIGHT = 700

FPS = 60
ANIMATION_FRAMES = 5

GAME_TIME = 60

COLLISION_FACTOR = .8
INVULNERBILITY_FRAMES = 240

ROOT_PATH = 'data\states\Feng_level\Assets'
SOUND_PATH = 'Sounds'
ANIMATION_PATH = 'Animations'

class Entity:
    def __init__(self, x = 0, y = 0, size = BLOCK_SIZE):
        self.size = size
        self.rect = pygame.Rect(x, y, self.size, self.size)

        self.frames = None
        self.animations = {'idle': None}
        self.state = 'idle'

    def center(self):
        self.rect.x += BLOCK_SIZE / 2 - self.size / 2
        self.rect.y += BLOCK_SIZE / 2 - self.size / 2

    def animation_setup(self, animations):
        for state in self.animations.keys():
            self.animations[state] = animations[state]

        self.frames = self.animations[self.state]

    def update(self, display_surf):
        self.frames = self.animations[self.state]
        display_surf.blit(self.frames.next(), (self.rect.x, self.rect.y))

    def collide_rect(self, entity):
        collided = self.rect.scale_by(COLLISION_FACTOR). \
            colliderect(entity.rect.scale_by(COLLISION_FACTOR))
        return collided
    
    def is_player(self):
        return False
    
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

class Block(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)

class Bubble(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y, 18)

        self.counter = 0
        self.movement = 1
        # center place bubble to the center of the cell
        self.center()

        self.sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'bubble.mp3'))

    def float(self):
        if self.counter % 25 == 0:
            self.movement *= -1

        self.rect.y += self.movement

    def update(self, display_surf):
        self.counter += 1
        if self.counter % 5 == 0:
            self.float()
        super().update(display_surf)

class Character(Entity):
    def __init__(self, x = 0, y = 0, size = 48):
        super().__init__(x, y, size)
        # refer to Settings.py
        self.speed = PLAYER_SPEED

        self.animations.update({'move_left': None, 'move_right': None})
        self.center()

    def can_move(self, level, new_x, new_y):
        for block in level.blocks:
            if (Entity(new_x, new_y, size = self.size).collide_rect(block)):
                return False
        return new_x >= -10 and new_x <= CAMERA_WIDTH + 10 and new_y >= -10 and new_y <= CAMERA_HEIGHT + 10

    def move_right(self, level):
        self.state = 'move_right'
        new_x = self.rect.x + self.speed
        if self.can_move(level, new_x, self.rect.y):
            self.rect.x = new_x
            return True
        return False

    def move_left(self, level):
        self.state = 'move_left'
        new_x = self.rect.x - self.speed
        if self.can_move(level, new_x, self.rect.y):
            self.rect.x = new_x
            return True
        return False

    def move_up(self, level):
        new_y = self.rect.y - self.speed
        if self.can_move(level, self.rect.x, new_y):
            self.rect.y = new_y
            return True
        return False

    def move_down(self, level):
        new_y = self.rect.y + self.speed
        if self.can_move(level, self.rect.x, new_y):
            self.rect.y = new_y
            return True
        return False

class SpriteStripAnim(object):
    """sprite strip animator

    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim

        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.

        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.

        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        ss = SpriteSheet(filename)
        self.images = ss.load_strip(rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    def iter(self):
        self.i = 0
        self.f = self.frames
        return self
    
    def cur(self):
        return self.images[self.i - 1]
    
    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
    
    def __add__(self, ss):
        self.images.extend(ss.images)
        return self

class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except (pygame.error):
            print ('Unable to load spritesheet image:', filename)
            raise (SystemExit)
        
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class Spear(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y, 24)
               
        self.counter = 0
        self.movement = 1
        self.center()

        self.pickup_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'spear_pickup.mp3'))

    def float(self):
        if self.counter % 15 == 0:
            self.movement *= -1

        self.rect.y += self.movement

    def update(self, display_surf):
        self.counter += 1
        if self.counter % 5 == 0:
            self.float()
        super().update(display_surf)
    
class Naga(Character):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)

        self.counter = 0
        self.y_movement = 1
        self.state = 'move_left'
        self.center()

        self.death_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'naga_death.mp3'))


    def patrol(self):
        if self.counter % 120 == 0:
            self.y_movement *= -1
        
        if self.counter % 15 == 0:
            self.speed *= -1

        self.rect.y -= self.y_movement
        self.rect.x += self.speed
        self.counter += 1

    def update(self, display_surf):
        self.patrol()
        super().update(display_surf)

class Maze:
    def __init__(self):
        self.M = 18
        self.N = 10

        self.entities = [
            # This is a special level for little Sophia
            # [   1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            #     2, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1, 0, 0, 0, 4, 1, 6, 3,
            #     1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
            #     1, 0, 0, 0, 0, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 1, 0, 1,
            #     1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1,
            #     1, 0, 1, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
            #     1, 0, 0, 4, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1,
            #     1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
            #     0, 0, 0, 0, 1, 4, 1, 1, 0, 1, 4, 1, 0, 1, 0, 0, 7, 1,
            #     0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            # ],
            [   1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3,
                2, 0, 0, 0, 0, 5, 0, 0, 4, 0, 1, 0, 0, 0, 4, 1, 6, 0,
                1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 1, 4, 0, 0, 0, 5, 0, 1, 0, 1,
                1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1,
                1, 0, 1, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
                1, 0, 0, 4, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1,
                1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
                0, 0, 0, 0, 1, 4, 1, 1, 0, 1, 4, 1, 0, 1, 0, 0, 7, 1,
                0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            ],
            [
                2, 1, 1, 1, 0, 0, 0, 0, 0, 1, 4, 0, 0, 0, 1, 1, 1, 3, 
                0, 1, 4, 1, 0, 1, 4, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 
                0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 5, 0, 1, 0, 1, 4, 1, 0, 
                0, 0, 0, 5, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 
                1, 1, 1, 1, 1, 0, 0, 0, 1, 4, 1, 0, 0, 0, 0, 0, 1, 6, 
                1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 
                1, 4, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 
                1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 
                0, 0, 0, 0, 1, 4, 1, 0, 0, 0, 5, 0, 0, 0, 0, 7, 1, 4, 
                0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            ],
            [
                2, 0, 1, 4, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 6, 3, 
                1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 
                0, 0, 0, 5, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 
                1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 4, 1, 0, 1, 
                1, 4, 0, 1, 0, 0, 1, 0, 0, 0, 5, 1, 0, 1, 1, 1, 1, 1, 
                1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 
                1, 0, 0, 0, 5, 0, 0, 1, 4, 0, 0, 1, 1, 1, 1, 1, 0, 1, 
                1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 7, 1, 0, 1, 
                0, 0, 0, 0, 1, 0, 0, 0, 0, 5, 0, 0, 0, 1, 1, 1, 0, 1, 
                0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
            ]
        ]

    def get_maze(self, level):
        return self.entities[level - 1]

class Level:

    def __init__(self,level):
        animation_loader = AssetsLoader()
        animation_loader.load_animations()
        self.animations = animation_loader.animations

        self.reset(level)

    def reset(self, level):
        self.entities = []
        self.blocks = []
        self.enemies = []
        self.bubbles = []

        self.cur_level = level
        self.lives_left = PLAYER_LIVES

        self.maze = Maze()
        self.register_level(level)


    def register_level(self, level):
        entities = self.maze.get_maze(level)
        bx = 0
        by = 0

        for i in range(0, self.maze.M * self.maze.N):
            match entities[bx + (by * self.maze.M)]:
                case 1:
                    block = Block(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(block)
                    self.blocks.append(block)
                case 2:
                    self.player = Player(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(self.player)
                case 3:
                    self.escape_point = EscapePoint(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(self.escape_point)
                case 4:
                    bubble = Bubble(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(bubble)
                    self.bubbles.append(bubble)
                case 5:
                    fish = Fish(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(fish)
                    self.enemies.append(fish)
                case 6:
                    naga = Naga(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(naga)
                    self.enemies.append(naga)
                case 7:
                    self.spear = Spear(bx * BLOCK_SIZE, by * BLOCK_SIZE)
                    self.register(self.spear)

            bx += 1
            if bx > self.maze.M - 1:
                bx = 0
                by += 1

    def register(self, entity):
        entity.animation_setup(self.animations[entity.__class__.__name__])
        self.entities.append(entity)

    def escaped(self):
        return self.player.collide_rect(self.escape_point)
    
    def remove_entity(self, entity):
        try:
            self.entities.remove(entity)
        except ValueError:
            pass
        try:
            self.bubbles.remove(entity)
        except ValueError:
            pass
        try:
            self.enemies.remove(entity)
        except ValueError:
            pass

    def update(self, display_surf):
        for entity in self.entities:
            entity.update(display_surf)
        
        for bubble in self.bubbles:
            if self.player.collide_rect(bubble):
                self.remove_entity(bubble)
                self.lives_left = min(PLAYER_LIVES, self.lives_left + 2)
                bubble.sound.play()
        
        if self.player.collide_rect(self.spear):
            self.remove_entity(self.spear)
            self.player.armed = True
            self.spear.pickup_sound.play()

        if self.player.freeze is False:
            for enemy in self.enemies:
                if self.player.collide_rect(enemy):
                    if self.player.armed == True:
                        self.remove_entity(enemy)
                        self.player.armed = False
                        enemy.death_sound.play()
                        self.player.freeze = True
                    else:
                        self.lives_left -= 1
                        self.player.hurt_sound.play()
                        self.player.freeze = True
        else:
            self.player.counter += 1
            if self.player.counter % 60 == 0:
                self.player.freeze = False

    def next(self):
        self.reset(self.cur_level + 1)

class HealthBar:
    def __init__(self):
        heart = pygame.image.load(os.path.join(ROOT_PATH, 'lives.png')).convert_alpha()
        heart.set_colorkey(heart.get_at((0, 0)), pygame.RLEACCEL)
        self.hrt_width, self.hrt_height = 24, 24
        self.heart = pygame.transform.scale(heart, (self.hrt_width, self.hrt_height)) # 330w x 197h

        life_bg = pygame.image.load(os.path.join(ROOT_PATH, 'lives_bg.png')).convert_alpha()
        life_bg.set_colorkey(life_bg.get_at((0, 0)), pygame.RLEACCEL)
        self.bg_width, self.bg_height = 249, 104
        self.life_bg = pygame.transform.scale(life_bg, (self.bg_width, self.bg_height)) # 249w x 104h

        self.display_x = 10
        self.display_y = 585

    def draw(self, lives_left, surface):
        life_rect = self.life_bg.get_rect()

        hrt_x = self.display_x + life_rect[0] + 50
        hrt_y = (life_rect[1] + (self.bg_height/2))-self.hrt_height/2 + 585
        #--^top of the bg_img + half of the bg_img height, - half of the heart height to get centered properly

        surface.blit(self.life_bg, (self.display_x, self.display_y))

        next = 0
        if lives_left > 0:
            for i in range(lives_left):
                surface.blit(self.heart, (hrt_x + next, hrt_y))
                next += 34

class Game:
    clock = pygame.time.Clock()

    def __init__(self):
        pygame.init()
        # sound effect
        pygame.mixer.init()
        self._running = True
        self.display_surf = None
        self.level = None
        # get the time
        self.start_time = pygame.time.get_ticks()
        # assign 3 to max_level
        self.max_level = 3

    def on_init(self, level):
        self.display_surf = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('The Cult of Barnacles')
        # refer to the Settings.py
        pygame.mixer.music.load(os.path.join(ROOT_PATH, SOUND_PATH, 'bg_music.mp3'))
        # pygame.mixer.music.load('data\states\Feng_level\Assets\Sounds\\bg_music.mp3')
        # 1 to loop, start from 0.0
        pygame.mixer.music.play(1, 0.0)

        self.level = Level(level)
        self.healthbar = HealthBar()

        self.ss_success = pygame.image.load(os.path.join(ROOT_PATH, 'splash_pass.png')).convert()
        self.ss_success = pygame.transform.scale(self.ss_success, (CAMERA_WIDTH, CAMERA_HEIGHT))
        self.success_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'pass.mp3'))

        self.ss_failed = pygame.image.load(os.path.join(ROOT_PATH, 'splash_fail.png')).convert()
        self.ss_failed = pygame.transform.scale(self.ss_failed, (CAMERA_WIDTH, CAMERA_HEIGHT))
        self.fail_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'fail.mp3'))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def on_loop(self):
        self.calc_life()
        self.clock.tick(FPS)

    def on_render(self):
        self.bg_surf = pygame.image.load(os.path.join(ROOT_PATH, 'background.png')).convert()
        self.bg_surf = pygame.transform.scale(self.bg_surf, (CAMERA_WIDTH, CAMERA_HEIGHT))
        self.display_surf.blit(self.bg_surf, (0, 0))

        self.level.update(self.display_surf)
        self.healthbar.draw(self.level.lives_left, self.display_surf)

        pygame.display.update()


    def on_win(self):
        self.display_surf.blit(self.ss_success, (0, 0))
        self.success_sound.play()
        pygame.display.update()
        self._running = False

        # if self.level.cur_level == self.max_level:
        #     self._running = False
        # else:
        #     pygame.time.wait(3000)
        #     self.start_time = pygame.time.get_ticks()
        #     self.level.next()

    def on_lose(self):
        self.display_surf.blit(self.ss_failed, (0, 0))
        self.fail_sound.play()
        pygame.display.update()
        self._running = False

    def calc_life(self):
        if (pygame.time.get_ticks() - self.start_time) > 5000:
            self.level.lives_left -= 1
            self.start_time = pygame.time.get_ticks()

    def on_execute(self, level):
        if self.on_init(level) is False:
            self._running = False

        while True:
            for event in pygame.event.get():
                self.on_event(event)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.level.player.move_right(self.level)

            if keys[pygame.K_LEFT]:
                self.level.player.move_left(self.level)

            if keys[pygame.K_UP]:
                self.level.player.move_up(self.level)

            if keys[pygame.K_DOWN]:
                self.level.player.move_down(self.level)

            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            if self.level.escaped() and self.level.lives_left > 0:
                self.on_win()
                
            if self.level.lives_left == 0:
                self.on_lose()

            if self._running:
                self.on_loop()
                self.on_render()

class Entity:
    def __init__(self, x = 0, y = 0, size = BLOCK_SIZE):
        self.size = size
        self.rect = pygame.Rect(x, y, self.size, self.size)

        self.frames = None
        self.animations = {'idle': None}
        self.state = 'idle'

    def center(self):
        self.rect.x += BLOCK_SIZE / 2 - self.size / 2
        self.rect.y += BLOCK_SIZE / 2 - self.size / 2

    def animation_setup(self, animations):
        for state in self.animations.keys():
            self.animations[state] = animations[state]

        self.frames = self.animations[self.state]

    def update(self, display_surf):
        self.frames = self.animations[self.state]
        display_surf.blit(self.frames.next(), (self.rect.x, self.rect.y))

    def collide_rect(self, entity):
        collided = self.rect.scale_by(COLLISION_FACTOR). \
            colliderect(entity.rect.scale_by(COLLISION_FACTOR))
        return collided
    
    def is_player(self):
        return False
    
class EscapePoint(Entity):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)

class Fish(Character):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y, 24)

        self.counter = 0
        self.x_movement = 1
        self.state = 'move_right'

        self.death_sound = pygame.mixer.Sound(os.path.join(ROOT_PATH, SOUND_PATH, 'fish_death.mp3'))

    def patrol(self):
        if self.counter % 15 == 0:
            self.x_movement *= -1
        
        if self.counter % 120 == 0:
            self.speed *= -1
            if self.state == 'move_left':
                self.state = 'move_right'
            else:
                self.state = 'move_left'

        self.rect.y += self.x_movement
        self.rect.x += self.speed
        self.counter += 1

    def update(self, display_surf):
        self.patrol()
        super().update(display_surf)





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
        self.persist = {}

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
