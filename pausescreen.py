""" the screen that appears when the player pauses the game.
"""

from gamescreen import *
from mappane import *

class PauseScreen(GameScreen):
	""" TODO: docstring """
	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager) #TODO
		self.player = player
		self.map_pane = MapPane(player, 40, 40) #TODO: other panes
		self.pause_panes = [self.map_pane]
		self.current_pane = self.map_pane

	def update(self):
		self.draw_bg()
		x, y = self.current_pane.x, self.current_pane.y
		self.screen_image.blit(self.current_pane.pane_image, (x, y))