""" The controls used when in the player's inventory.
"""

from controls import *

class InventoryControls(Controls):
	""" MapControls( Player ) -> MapControls

	The inventory controls are used to make item-based changes or to exit the inventory screen.

	Attributes:

	player: The Player whose inventory is controlled via these controls.
	"""

	def __init__(self, player):
		Controls.__init__(self)
		self.initialize_control_map(INVENTORY_CONTROL_MAP)
		self.player = player

	def unpause(self, key, toggle):
		""" mc.unpause( str, bool ) -> None

		When the player presses enter, resume the game.
		"""
		if toggle:
			self.player.unpause_game()

	def move_cursor(self, key, toggle):
		""" mc.move_cursor( str, bool ) -> None

		Move the pause cursor from its current position.
		"""
		if toggle: pass #TODO

unpause = InventoryControls.unpause
move_cursor = InventoryControls.move_cursor

INVENTORY_CONTROL_MAP = {
	K_RETURN:unpause,
	K_i:unpause,
	K_LEFT:move_cursor,
	K_RIGHT:move_cursor
}