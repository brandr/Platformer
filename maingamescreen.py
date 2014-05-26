""" the main screen for playing the game. Most of the player's actions take place here.
"""

from gamescreen import *

class MainGameScreen(GameScreen):

	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager)
		self.width, self.height = WIN_WIDTH, WIN_HEIGHT
		self.player = player

	def update(self):
		self.draw_bg()
		self.level_update()
		self.effects_update()

	def level_update(self):
		self.player.current_level.update(False, False, False, False, False, False)

	def effects_update(self):
		pass 

	def clear(self):
		self.contents = Surface((self.width, self.height))