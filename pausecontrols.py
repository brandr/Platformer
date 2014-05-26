""" The controls used when the game is paused.
"""

from controls import *

class PauseControls(Controls):
	""" TODO: docstring"""

	def __init__(self, player):
		Controls.__init__(self)
		self.initialize_control_map(PAUSE_CONTROL_MAP)
		self.player = player

	def unpause(self, key, toggle):
		if toggle:
			self.player.unpause_game()

unpause = PauseControls.unpause

PAUSE_CONTROL_MAP = {
	K_RETURN:unpause
}