""" The screen that appears when the player begins changing the game controls.
"""

from selectcontrols import SelectControls
from selectscreen import SelectScreen, CONTROLS, SCREEN_DATA_MAP, OPTIONS_COORDS
from dialog import WHITE, BLACK
from controls import Controls
import pygame
from pygame import Surface, Color, font
from pygame.locals import *
import ConfigParser

RED = Color("#FF0000")

class ControlsScreen(SelectScreen):
	""" ControlsScreen( ControlManager, Player) -> ControlsScreen

	The ControlsScreen is a slightly modified SelectScreen that allows the player
	to change the game controls by setting specific actions to keys and saving these
	relationships to a .ini file to be loaded when the game starts.

	Attributes:

	level_image: A Surface representing the level the player was on the moment it was paused.
	"""

	def __init__(self, control_manager, player):
		level_image = player.current_level.screen
		SelectScreen.__init__(self, control_manager, player, level_image, CONTROLS, CONTROLS_OPTIONS, CONTROLS_OPTION_METHODS ) 
		self.title = "Controls"
		self.option_font_size = 18
		self.control_map = self.load_control_map()
		self.setting_key = False

	def load_control_map(self):
		""" cs.load_control_map( ) -> { str:str }
		
		Returns a dict mapping actions to key inputs.
		"""
		control_map = []
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		controls = config.options("controls")
		for c in controls:
			try: control_map.append(config.get("controls", c))
			except:
				print "ERROR: missing control settings. Check config.ini."
				raise(SystemExit)
		return control_map

	def select(self):
		""" cs.select( ) -> None

		Select the current option, executing its associated action.
		This only works if a control key is not already selected.
		"""
		if not (self.setting_key):
			SelectScreen.select(self)
			return

	def draw_select_pane(self):
		""" cs.draw_select_pane( ) -> Surface

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
		""" cs.draw_select_options_pane( ) -> Surface

		Draws a pane for control selection.
		"""
		pane = SelectScreen.draw_select_options_pane(self)
		self.display_controls(pane)
		if self.setting_key: self.draw_key_selection(pane)
		return pane

	def display_controls(self, pane):
		""" cs.display_controls( Surface ) -> None

		Show the current control settings.
		"""
		text_font = font.Font("./fonts/FreeSansBold.ttf", self.option_font_size)
		i = 0
		for c in self.control_map:
			text_image = text_font.render(c, 1, BLACK)
			pane.blit(text_image, ( 300, 8 + 26*i ))
			i += 1

	def draw_key_selection(self, pane):
		""" cs.draw_key_selection( Surface ) -> None

		Visually show which key is selected.
		"""
		y = self.option_index*(self.option_font_size + 8) + 2
		points = [ ( 296, y ), ( 380, y ), ( 380, y + 32 ), ( 296, y + 32 ) ]
		pygame.draw.lines( pane, RED , True, points, 2 )

	# Controls methods

	def begin_set_key(self):
		""" cs.begin_set_key( ) -> None

		Begin setting the key used to perform some action ingame.
		"""
		self.setting_key = True
		self.player.current_level.screen_manager.set_controls(ControlSettingControls(self))

	def set_key(self, key):
		""" cs.set_key( ) -> None

		Take the action associated with the current option index and set its key to the given key.
		"""
		if key in self.control_map:
			index = self.control_map.index(key)
			current_key = self.control_map[self.option_index]
			self.control_map[index] = current_key
			self.control_map[self.option_index] = key
			return
		self.control_map[self.option_index] = key

	def restore_defaults(self):
		""" cs.restore_defaults( ) -> None

		Restore control settings to the defaults.
		"""
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		controls = config.options("default_controls")
		index = 0
		for c in controls:
			try: 
				self.control_map[index] = config.get("default_controls", c)
				index += 1
			except:
				print "ERROR: missing control settings. Check config.ini."
				raise(SystemExit)

	def default_controls(self):
		"""cs.default_controls( ) -> [ str ]

		Return a list of the default control settings.
		"""
		control_list = []
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		controls = config.options("default_controls")
		for c in controls:
			try: control_list.append( config.get("default_controls", c) )
			except:
				print "ERROR: missing control settings. Check config.ini."
				raise(SystemExit)
		return control_list

	def confirm(self):
		""" cs.confirm( ) -> None

		Confirm changes to controls and return to the options menu.
		"""
		# TODO: write the current control scheme to config.ini
		default_controls = self.default_controls()
		config = ConfigParser.RawConfigParser()
		config.add_section('controls')
		config.add_section('default_controls')
		for i in xrange(len(CONTROLS_OPTIONS) - 2): 
			config.set('controls', CONTROLS_OPTIONS[i], self.control_map[i])
			config.set('default_controls', CONTROLS_OPTIONS[i], default_controls[i] )
		with open('config.ini', 'wb') as configfile: config.write(configfile)
		self.player.current_level.screen_manager.switch_to_options_screen(self.player)


# control constants

MOVE_LEFT = "Move left"
MOVE_RIGHT = "Move right"
MOVE_UP = "Move up"
MOVE_DOWN = "Move down"
JUMP = "Jump"
SPRINT = "Sprint"
MELEE_ATTACK = "Melee Attack"
RANGED_ATTACK = "Ranged Attack"
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
	JUMP, SPRINT, MELEE_ATTACK, RANGED_ATTACK, INTERACT,
	PAUSE, INVENTORY, MAP,
	TOGGLE_LANTERN_LEFT, TOGGLE_LANTERN_RIGHT, LANTERN_ABILITY,
	RESTORE_DEFAULTS, CONFIRM
]

begin_set_key = ControlsScreen.begin_set_key

# might be easier to do this by dictating that all but the last 2 are begin_set_key
CONTROLS_OPTION_METHODS = [
	begin_set_key, begin_set_key, begin_set_key, begin_set_key,
	begin_set_key, begin_set_key, begin_set_key, begin_set_key, begin_set_key,
	begin_set_key, begin_set_key, begin_set_key,
	begin_set_key, begin_set_key, begin_set_key,
	ControlsScreen.restore_defaults, ControlsScreen.confirm
]

class ControlSettingControls(Controls):
	""" ControlSettingControls( ControlsScreen ) -> ControlSettingControls

	Special controls for changing which buttons correspond to which actions.
	"""
	def __init__(self, screen):
		Controls.__init__(self)
		control_map = self.build_control_map()
		self.initialize_control_map(control_map)
		self.screen = screen

	def build_control_map(self):
		""" csc.initialize_control_map( ) -> { str:method }

		Create a control map that will allow the player to associate actions with valid keys.
		""" 
		control_map = {}
		for key in VALID_KEYS: control_map[key] = ControlSettingControls.set_key
		return control_map

	def set_key(self, key, toggle):
		""" csc.set_key( str, bool ) -> None

		Set the currently selected action to the inputted key.
		"""
		if toggle:
			key_string = VALID_KEYS[key]
			self.screen.set_key(key_string)
			controls = SelectControls(self.screen.player)
			self.screen.player.current_level.screen_manager.set_controls(controls)
			self.screen.setting_key = False

VALID_KEYS = {
	K_UP:"up", K_DOWN:"down", K_LEFT:"left", K_RIGHT:"right",
	K_SPACE:"space", K_LCTRL:"control", K_RETURN:"return",
	K_a:"a", K_b:"b", K_c:"c", K_d:"d", K_e:"e", K_f:"f", K_g:"g", K_h:"h", K_i:"i", K_j:"j", K_l:"l", K_m:"m", 
	K_n:"n", K_o:"o", K_p:"p", K_q:"q",	K_r:"r", K_s:"s", K_t:"t", K_u:"u", K_v:"v", K_w:"w", K_x:"x", K_z:"z"
}