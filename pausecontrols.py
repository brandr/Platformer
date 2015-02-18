""" The controls used when the game is paused.
"""

from controls import *

class PauseControls(Controls):
	""" PauseControls( Player ) -> PauseControls

	The pause controls are currently limited to pressing enter to resume the game, but if menus are
	added to the pause screen then this will change.

	Attributes:

	player: The Player to be shown on the map screen while the game is paused.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.initialize_control_map(PAUSE_CONTROL_MAP)
		self.player = player

	def select(self, key, toggle):
		""" pc.select( str, bool ) -> None

		Select the current pause option.
		"""
		if toggle: self.control_manager.screen.select()

	def move_cursor(self, key, toggle):
		""" pc.move_cursor( str, bool ) -> None

		Move the pause cursor from its current position.
		"""
		if toggle: 
			direction = PAUSE_DIRECTION_MAP[key]
			self.control_manager.screen.move_cursor(direction)

select = PauseControls.select
move_cursor = PauseControls.move_cursor

PAUSE_CONTROL_MAP = {
	K_RETURN:select,
	K_LEFT:move_cursor,
	K_RIGHT:move_cursor,
	K_UP:move_cursor,
	K_DOWN:move_cursor
}

PAUSE_DIRECTION_MAP = {
	K_LEFT:-1,
	K_RIGHT:1,
	K_UP:-1,
	K_DOWN:1
}