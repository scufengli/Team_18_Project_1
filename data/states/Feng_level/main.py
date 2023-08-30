# import Game class from the game package
from .Game import Game


# entry point
def run(level):
    game = Game()
    return game.on_execute(level), True

    