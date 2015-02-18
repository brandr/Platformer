""" An abstract control type used to navigate a set of text options.
"""

from controls import *

class SelectControls(Controls):
	""" SelectControls( Player ) -> SelectControls

	Select controls can be used in various screens to manipulate a cursor and select an option from a set of options.

	Attributes:

	player: The Player to be shown on the map screen while the game is paused.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.initialize_control_map(SELECT_CONTROL_MAP)
		self.player = player

	def select(self, key, toggle):
		""" sc.select( str, bool ) -> None

		Select the current option.
		"""
		if toggle: self.control_manager.screen.select()

	def move_cursor(self, key, toggle):
		""" sc.move_cursor( str, bool ) -> None

		Move the cursor from its current position.
		"""
		if toggle: 
			direction = SELECT_DIRECTION_MAP[key]
			self.control_manager.screen.move_cursor(direction)

select = SelectControls.select
move_cursor = SelectControls.move_cursor

SELECT_CONTROL_MAP = {
	K_RETURN:select,
	K_LEFT:move_cursor,
	K_RIGHT:move_cursor,
	K_UP:move_cursor,
	K_DOWN:move_cursor
}

SELECT_DIRECTION_MAP = {
	K_LEFT:-1,
	K_RIGHT:1,
	K_UP:-1,
	K_DOWN:1
}