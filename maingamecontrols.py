""" Handles the controls used when the player is in the main game.
"""

from controls import *

class MainGameControls(Controls):
	""" MainGameControls( Player ) -> MainGameControls

	Can handlre various contexts, but they should all be associated with
	the main game.

	Attributes:

	Player: the player associated with these controls. 
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.player = player
		self.direction_map = {
			K_LEFT:self.player.left, K_RIGHT:self.player.right, K_UP:self.player.up, K_DOWN:self.player.down,
			K_SPACE:self.player.space, K_LCTRL:self.player.control
		}
		self.initialize_control_map(MAIN_GAME_CONTROL_MAP)

	def move_up(self, key, toggle):
		self.player.up = toggle

	def move_down(self, key, toggle):
		self.player.down = toggle

	def move_left(self, key, toggle):
		self.player.left = toggle

	def move_right(self, key, toggle):
		self.player.right = toggle

	def move_space(self, key, toggle):
		self.player.space = toggle

	def move_control(self, key, toggle):
		self.player.control = toggle

move_up = MainGameControls.move_up
move_down = MainGameControls.move_down
move_left = MainGameControls.move_left
move_right = MainGameControls.move_right

move_space = MainGameControls.move_space
move_control = MainGameControls.move_control

MAIN_GAME_CONTROL_MAP = { 
	K_UP:move_up, K_DOWN:move_down, K_LEFT: move_left, K_RIGHT:move_right,
	K_SPACE:move_space, K_LCTRL:move_control
}