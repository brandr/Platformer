""" Handles the controls used when the player is in the main game.
"""

from controls import *

class MainGameControls(Controls):
	""" MainGameControls( Player ) -> MainGameControls

	Can handle various contexts, but they should all be associated with
	the main game.

	Attributes:

	player: the player associated with these controls. 

	direction_map: the buttons used in the main game (as strings) mapped to the actions they cause.
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
		""" mgc.move_up( str, bool ) -> None

		Up key action.
		"""
		self.player.up = toggle

	def move_down(self, key, toggle):
		""" mgc.move_down( str, bool ) -> None

		Down key action.
		"""
		self.player.down = toggle

	def move_left(self, key, toggle):
		""" mgc.move_left( str, bool ) -> None

		Left key action.
		"""
		self.player.left = toggle

	def move_right(self, key, toggle):
		""" mgc.move_right( str, bool ) -> None

		Right key action.
		"""
		self.player.right = toggle

	def move_space(self, key, toggle):
		""" mgc.move_space( str, bool ) -> None

		Space key action.
		"""
		self.player.space = toggle

	def move_control(self, key, toggle):
		""" mgc.move_control( str, bool ) -> None

		Control key action.
		"""
		self.player.control = toggle

	def press_x(self, key, toggle):
		""" mgc.press_x( str, bool ) -> None

		x key action.
		"""
		self.player.x = toggle

	def press_z(self, key, toggle):
		""" mgc.press_z( str, bool ) -> None

		z key action.
		"""
		if toggle:
			self.player.temp_z_method()	#consider making this work like every other button, or making the x key work like this.

	def pause(self, key, toggle):
		""" mgc.pause( str, bool ) -> None

		Tell the player to pause the game.
		"""
		if(toggle):
			self.player.pause_game()

move_up = MainGameControls.move_up
move_down = MainGameControls.move_down
move_left = MainGameControls.move_left
move_right = MainGameControls.move_right

move_space = MainGameControls.move_space
move_control = MainGameControls.move_control

press_x = MainGameControls.press_x
press_z = MainGameControls.press_z

pause = MainGameControls.pause

MAIN_GAME_CONTROL_MAP = { 
	K_UP:move_up, K_DOWN:move_down, K_LEFT: move_left, K_RIGHT:move_right,
	K_SPACE:move_space, K_LCTRL:move_control,
	K_x:press_x,
	K_z:press_z,
	K_RETURN:pause
}