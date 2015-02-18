""" The screen that appears when the player accesses game options while paused.
"""

from selectscreen import SelectScreen, OPTIONS, SCREEN_DATA_MAP, OPTIONS_COORDS
from dialog import WHITE, BLACK
import pygame
from pygame import Surface, font 

class OptionsScreen(SelectScreen):
	""" OptionsScreen( ControlManager, Player) -> OptionsScreen

	The options screen shows a set of game options the player can change.
	Since it is a type of SelectScreen, these options are represented as a vertical list.

	Attributes:

	level_image: A Surface representing the level the player was on the moment it was paused.
	"""
#TODO: add more options
# change controls
# adjust volume (will do nothing at the moment)

	def __init__(self, control_manager, player):
		level_image = player.current_level.screen
		SelectScreen.__init__(self, control_manager, player, level_image, OPTIONS, OPTIONS_OPTIONS, OPTIONS_OPTION_METHODS ) 
		self.title = "Options"

	def draw_select_pane(self):
		""" os.draw_select_pane( ) -> Surface

		Draw an image representing the pause pane.
		"""
		pane = SelectScreen.draw_select_pane(self)
		text_font = font.Font("./fonts/FreeSansBold.ttf", 28)
		text_image = text_font.render(self.title, 1, BLACK)
		pane.blit(text_image, ( 100, 20 ))
		coords = SCREEN_DATA_MAP[OPTIONS][OPTIONS_COORDS]
		pane.blit(self.draw_select_options_pane(), (coords[0], coords[1]))	
		return pane

	# Options methods

	def controls(self):
		""" os.controls( ) -> None

		Start changing the control settings from the options screen.
		"""
		self.player.current_level.screen_manager.switch_to_controls_screen(self.player)

	def option_return(self):
		""" os.option_return( ) -> None

		Return to the normal pause menu.
		"""
		#TODO: may want to confirm changes here, or make this a cancel button and have another button to confirm changes.
		self.player.current_level.screen_manager.switch_to_pause_screen(self.player, 1)

# options contstants

CONTROLS = "Controls"
OPTION_RETURN = "Return"
OPTIONS_OPTIONS = [CONTROLS, OPTION_RETURN]

OPTIONS_OPTION_METHODS = [
	OptionsScreen.controls,
	OptionsScreen.option_return
]

