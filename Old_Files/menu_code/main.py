from game import Game


g = Game()
#inv = Invetory()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
