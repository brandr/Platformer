""" The controls used when the game is paused and options are selected.
"""

from controls import *

class OptionsControls(Controls):
	""" OptionsControls( Player ) -> OptionsControls

	The options controls are used to alter ingame options such as the control scheme.

	Attributes:

	player: The Player who paused the game. Used as a reference point to find other objects.
	"""
	def __init__(self, player):
		Controls.__init__(self)
		self.initialize_control_map(OPTIONS_CONTROL_MAP)
		self.player = player

	def close_options(self, key, toggle):
		""" oc.close_options( str, bool ) -> None

		Close the options pane and return to the normal pause menu.
		"""
		if toggle: self.player.current_level.screen_manager.switch_to_pause_screen(self.player, 1)

OPTIONS_CONTROL_MAP = {
	K_RETURN:OptionsControls.close_options #TEMP (change controls once options pane is fleshed out)
}