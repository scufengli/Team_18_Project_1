import pygame as pg 
import sys
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI

class Game:
	def __init__(self):

		# GAME ATTRIBUTES
		self.max_level = 2
		self.max_health = 5
		self.curr_health = 5
		self.coins = 0 

		# AUDIO
		self.BGM = pg.mixer.Sound('Audio\main_menu_BG_music.mp3')

		# OVERWORL CREATION
		self.overworl = Overworld(0,self.max_level, screen, self.create_level)
		self.status = 'OVERWORLD'

		# USER INTERFACE 
		self.ui = UI(screen)

	def create_level(self,current_level):
		self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
		self.status = 'level'
		self.BGM.stop()

	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		self.BGM.play(loops = -1)

	def change_coins(self,amount):
		self.coins += amount

	def change_health(self,amount):
		self.cur_health += amount

	def check_game_over(self):
		if self.cur_health <= 0:
			self.cur_health = 100
			self.coins = 0
			self.max_level = 0
			self.overworld = Overworld(0,self.max_level,screen,self.create_level)
			self.status = 'overworld'
			self.BGM.play(loops = -1)

	def run(self):
		if self.status == 'overworld':
			self.overworld.run()
		else:
			self.level.run()
			self.ui.show_health(self.cur_health,self.max_health)
			self.ui.show_coins(self.coins)
			self.check_game_over()

# Pygame setup
pg.init()
screen = pg.display.set_mode((screen_width,screen_height))
clock = pg.time.Clock()
game = Game()

while True:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
	
	screen.fill('black')
	game.run()

	pg.display.update()
	clock.tick(60)