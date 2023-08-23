import pygame as pg
from ..tools import*
from ..prepare import*
from ..states.u_water_level.Game import*

from .u_water_level.Player import*

from .u_water_level.Maze import* 
from .u_water_level.EscapePoint import* 
from .u_water_level.Settings import*

class Underwater(tools._State):
    """This is a prototype class for States.  All states should inherit from it.
    No direct instances of this class should be created. get_event and update
    must be overloaded in the childclass.  startup and cleanup need to be
    overloaded when there is data that must persist between States."""
    def __init__(self):
        tools._State.__init__(self) 
        self.clock = pg.time.Clock()
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.next = "MAINMENU" #==== Note 1 ====#
        self.timeout = 5
        self.player = Player()
        self.escape_point = EscapePoint(1130, 0)
        self._bg_surf = pygame.image.load("resources/graphics/u_water_graphics/background.jpeg").convert()
        self.maze = Maze()
        self._block_surf = pygame.image.load("resources/graphics/u_water_graphics/block.png").convert()

        self.clock.tick(FPS)

        # self.persist = {}
        self.display_surface = mp.SCREEN
        self._running = True
        self._player_surf = None
        self._escape_surf = None
        self.start_time = pygame.time.get_ticks()
        self._bg_surf = pygame.transform.scale(self._bg_surf, (mp.screen_size))

        self._block_surf = pygame.transform.scale(self._block_surf, (BLOCK_SIZE, BLOCK_SIZE))

        self.ss_success = pygame.image.load("resources/graphics/u_water_graphics/SplashScreenPassed.jpeg").convert()
        self.ss_success = pygame.transform.scale(self.ss_success, (mp.screen_size))

        self.ss_failed = pygame.image.load("resources/graphics/u_water_graphics/SplashScreenFailed.jpeg").convert()
        self.ss_failed = pygame.transform.scale(self.ss_failed, (mp.screen_size))
        
    def on_loop(self):
        self._player_surf = self.player.frames.next()
        self._escape_surf = self.escape_point.frames.next()

    def on_render(self):
        mp.SCREEN.blit(self._bg_surf, (0, 0))
        mp.SCREEN.blit(self._player_surf, (self.player.x, self.player.y))
        self.maze.draw(mp.SCREEN, self._block_surf)
        self.escape_point.draw(mp.SCREEN, self._escape_surf)
        pygame.display.flip()

    def update(self, surface, keys, current_time, time_delta):
        """Updates the splash screen."""
        self.current_time = current_time
        surface.blit(self.image,self.rect)
        self.cover.set_alpha(self.cover_alpha)
        self.cover_alpha = max(self.cover_alpha-self.alpha_step,0)
        surface.blit(self.cover,(0,0))
        if self.current_time-self.start_time > 1000.0*self.timeout:
            self.done = True

    def on_win(self):
        mp.SCREEN.blit(self.ss_success, (0, 0))
        pygame.display.flip()
        self.done = True

    def on_lose(self):
        mp.SCREEN.blit(self.ss_failed, (0, 0))
        pygame.display.flip()


    def get_seconds(self):
        return (pygame.time.get_ticks() - self.start_time) / 1000

    def run(self):
        self.on_loop()
        self.on_render()


    # def on_execute(self):
    #     if self.on_init() is False:
    #         self._running = False

    #     while True:
    #         pass
    #     #     pygame.event.pump()



    def get_event(self, event):
        """Processes events that were passed from the main event loop.
        Must be overloaded in children."""
        keys = pygame.key.get_pressed()

        if keys[K_RIGHT]:
            self.player.moveRight(self.maze)

        if keys[K_LEFT]:
            self.player.moveLeft(self.maze)

        if keys[K_UP]:
            self.player.moveUp(self.maze)

        if keys[K_DOWN]:
            self.player.moveDown(self.maze)

        if keys[K_ESCAPE]:
            self._running = False

        if self.player.is_escaped(self.escape_point):
            self.on_win()
            self._running = False

        if self.get_seconds() > GAME_TIME:
            self.on_lose()
            self._running = False

        if self._running:
            self.on_loop()
            self.on_render()

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

    def update(self, surface, keys, current_time, dt):
        """Update function for state.  Must be overloaded in children."""
        self.run()
        pass