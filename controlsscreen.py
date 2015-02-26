""" The screen that appears when the player begins changing the game controls.
"""

from selectscreen import SelectScreen, CONTROLS, SCREEN_DATA_MAP, OPTIONS_COORDS
from dialog import WHITE, BLACK
import pygame
from pygame import Surface, font
import ConfigParser


class ControlsScreen(SelectScreen):
	""" ControlsScreen( ControlManager, Player) -> ControlsScreen

	TODO: descritpiton

	Attributes:

	level_image: A Surface representing the level the player was on the moment it was paused.
	"""

	def __init__(self, control_manager, player):
		level_image = player.current_level.screen
		SelectScreen.__init__(self, control_manager, player, level_image, CONTROLS, CONTROLS_OPTIONS, CONTROLS_OPTION_METHODS ) 
		self.title = "Controls"
		self.option_font_size = 18
		self.control_map = self.load_control_map()

	def load_control_map(self):
		""" os.load_control_map( ) -> { str:str }
		
		Returns a dict mapping actions to key inputs.
		"""
		control_map = {}
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		controls = config.options("controls")
		for c in controls:
			try: control_map[c] = config.get("controls", c)
			except:
				print "ERROR: missing control settings. Check config.ini."
				raise(SystemExit)
		return control_map

	def draw_select_pane(self):
		""" os.draw_select_pane( ) -> Surface

		Draw an image representing the pause pane.
		"""
		pane = SelectScreen.draw_select_pane(self)
		text_font = font.Font("./fonts/FreeSansBold.ttf", 28)
		text_image = text_font.render(self.title, 1, BLACK)
		pane.blit(text_image, ( 100, 20 ))
		coords = SCREEN_DATA_MAP[CONTROLS][OPTIONS_COORDS]
		pane.blit(self.draw_select_options_pane(), (coords[0], coords[1]))
		return pane

	def draw_select_options_pane(self):
		""" os.draw_select_options_pane( ) -> Surface

		Draws a pane for control selection.
		"""
		pane = SelectScreen.draw_select_options_pane(self)
		self.display_controls(pane)
		return pane

	def display_controls(self, pane):
		""" os.display_controls( Surface ) -> None

		Show the current control settings.
		"""
		text_font = font.Font("./fonts/FreeSansBold.ttf", self.option_font_size)
		i = 0
		for c in self.control_map:
			text_image = text_font.render(self.control_map[c], 1, BLACK)
			pane.blit(text_image, ( 300, 8 + 26*i ))
			i += 1

	# Controls methods

	def begin_set_key(self):
		""" cs.begin_set_key( ) -> None

		Begin setting the key used to perform some action ingame.
		"""
		# TODO: used self.option_index to figure out which key needs to be set from a map and change the control scheme temporarily.
		# will need to make a new control scheme, possibly called ControlsControls
		return

	def restore_defaults(self):
		""" cs.restore_defaults( ) -> None

		Restore control settings to the defaults.
		"""
		return #TODO

	def confirm(self):
		""" cs.confirm( ) -> None

		Confirm changes to controls and return to the options menu.
		"""
		#TODO: write the current control scheme to config.ini
		self.player.current_level.screen_manager.switch_to_options_screen(self.player)


# control constants

MOVE_LEFT = "Move left"
MOVE_RIGHT = "Move right"
MOVE_UP = "Move up"
MOVE_DOWN = "Move down"
JUMP = "Jump"
SPRINT = "Sprint"
ATTACK = "Attack"
INTERACT = "Interact"
PAUSE = "Pause"
INVENTORY = "Inventory"
MAP = "Map"
TOGGLE_LANTERN_LEFT = "Toggle lantern left"
TOGGLE_LANTERN_RIGHT = "Toggle lantern right"
LANTERN_ABILITY = "Lantern ability"

RESTORE_DEFAULTS = "Restore defaults"
CONFIRM = "Confirm"

CONTROLS_OPTIONS = [
	MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN,
	JUMP, SPRINT, ATTACK, INTERACT,
	PAUSE, INVENTORY, MAP,
	TOGGLE_LANTERN_LEFT, TOGGLE_LANTERN_RIGHT, LANTERN_ABILITY,
	RESTORE_DEFAULTS, CONFIRM
]

begin_set_key = ControlsScreen.begin_set_key

CONTROLS_OPTION_METHODS = [
	begin_set_key, begin_set_key, begin_set_key, begin_set_key,
	begin_set_key, begin_set_key, begin_set_key, begin_set_key,
	begin_set_key, begin_set_key, begin_set_key,
	begin_set_key, begin_set_key, begin_set_key,
	ControlsScreen.restore_defaults, ControlsScreen.confirm
]

# TODO: make a dict to map control constants to specific actions.
# TODO: make a dict of additional display methods, to be called if the current title is in them.