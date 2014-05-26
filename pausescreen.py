""" the screen that appears when the player pauses the game.
"""

from gamescreen import *

class PauseScreen(GameScreen):
	""" TODO: docstring """
	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager) #TODO
		self.player = player
		self.pause_pane = self.build_pause_pane(player) 

	def update(self):
		self.draw_bg()
		self.screen_image.blit(self.pause_pane, (0, 0))

	def build_pause_pane(self, player):
		pause_pane = Surface((300, 300)) #TODO: probably make this its own class (and pass self.screen_image in, like is done with level)
		pause_pane.fill(Color("#FFFFFF")) #TEMP
		return pause_pane