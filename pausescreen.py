""" the screen that appears when the player pauses the game.
"""

from gamescreen import *
from mappane import *

class PauseScreen(GameScreen):
	""" PauseScreen( ControlManager, Player) -> PauseScreen

	Currently, the pause screen only shows the map pane. If there are multiple screens then this class
	will need to be restructured.

	Attributes:

	player: The player whose location is shown on the map pane.

	pause_panes: The set of panes shown onscreen while the game is paused.

	current_pane: The pane being shown right now.
	"""
	def __init__(self, control_manager, player):
		GameScreen.__init__(self, control_manager) #TODO
		self.player = player
		self.map_pane = MapPane(player, 40, 40) #TODO: other panes
		self.pause_panes = [self.map_pane]
		self.current_pane = self.map_pane

	def update(self):
		self.draw_bg()
		x, y = self.current_pane.x, self.current_pane.y
		self.current_pane.update()
		self.screen_image.blit(self.current_pane.pane_image, (x, y))