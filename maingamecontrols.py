""" Handles the controls used when the player is in the main game.
"""

from controls import *
import ConfigParser

LEFT, RIGHT, DOWN, UP, SPACE, CONTROL, X = "left", "right", "down", "up", "space", "control", "x"

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
		self.load_controls()

	def load_controls(self):
		""" mgc.load_controls( ) -> None

		Load the game's controls from config.ini.
		"""
		self.control_map = {}
		config = ConfigParser.ConfigParser()
		config.read("./config.ini")
		controls = config.options("controls")
		for c in controls:
			try: 
				key_value = KEY_VALUE_MAP[config.get("controls", c)]
				key_action = ACTION_MAP[c]
				self.control_map[key_value] = key_action
			except:
				print "ERROR: something is wrong with the saved control settings. Check config.ini."
				raise(SystemExit)

		#TODO make it so these controls load values from config.ini rather than using defaults.

	def move_up(self, key, toggle):
		""" mgc.move_up( str, bool ) -> None

		Up key action.
		"""
		self.player.button_press_map[UP] = toggle

	def move_down(self, key, toggle):
		""" mgc.move_down( str, bool ) -> None

		Down key action.
		"""
		self.player.button_press_map[DOWN] = toggle

	def move_left(self, key, toggle):
		""" mgc.move_left( str, bool ) -> None

		Left key action.
		"""
		self.player.button_press_map[LEFT] = toggle

	def move_right(self, key, toggle):
		""" mgc.move_right( str, bool ) -> None

		Right key action.
		"""
		self.player.button_press_map[RIGHT] = toggle

	def move_jump(self, key, toggle):
		""" mgc.move_jump( str, bool ) -> None

		Jump key action.
		"""
		self.player.button_press_map[SPACE] = toggle

	def move_sprint(self, key, toggle):
		""" mgc.move_sprint( str, bool ) -> None

		Sprint key action.
		"""
		self.player.button_press_map[CONTROL] = toggle

	def interact(self, key, toggle):
		""" mgc.interact( str, bool ) -> None

		Player interact action.
		"""
		self.player.button_press_map[X] = toggle
		
	def melee_attack(self, key, toggle):
		""" mgc.melee_attack( str, bool ) -> None

		Melee attack action.
		"""
		if toggle: self.player.temp_z_method()	#consider making this work like every other button, or making the x key work like this.

	def ranged_attack(self, key, toggle):
		""" mgc.ranged_attack( str, bool ) -> None

		Ranged attack action.
		"""
		if toggle: self.player.shoot() 

	def press_return(self, key, toggle):
		""" mgc.press_return( str, bool ) -> None

		Tell the player to pause the game.
		"""
		if(toggle):	self.player.pause_game()

	def open_inventory(self, key, toggle):
		""" mgc.open_inventory( str, bool ) -> None

		Opens the player's inventory.
		"""
		if toggle: self.player.open_inventory()

	def open_map(self, key, toggle):
		""" mgc.open_map( str, bool ) -> None

		Open the player's map.
		"""
		if toggle: self.player.open_map()

	def press_c(self, key, toggle):
		""" mgc.press_c( str, bool ) -> None

		c key action.
		"""
		if toggle: self.player.activate_lantern_ability()

	def press_q(self, key, toggle):
		""" mgc.press_q( str, bool ) -> None

		q key action.
		"""
		if toggle: self.player.toggle_lantern_mode(-1)

	def press_w(self, key, toggle):
		""" mgc.press_w( str, bool ) -> None

		w key action.
		"""
		if toggle: self.player.toggle_lantern_mode(1)

move_up = MainGameControls.move_up
move_down = MainGameControls.move_down
move_left = MainGameControls.move_left
move_right = MainGameControls.move_right

move_jump = MainGameControls.move_jump
move_sprint = MainGameControls.move_sprint

interact = MainGameControls.interact
melee_attack = MainGameControls.melee_attack
ranged_attack = MainGameControls.ranged_attack

open_inventory = MainGameControls.open_inventory
open_map = MainGameControls.open_map

press_c = MainGameControls.press_c
press_q = MainGameControls.press_q
press_w = MainGameControls.press_w

press_return = MainGameControls.press_return

KEY_VALUE_MAP = {
	"up":K_UP, "down":K_DOWN, "left":K_LEFT, "right":K_RIGHT,
	"space":K_SPACE, "control":K_LCTRL, "return":K_RETURN,
	"a":K_a, "b":K_b, "c":K_c, "d":K_d, "e":K_e, "f":K_f, "g":K_g, "h":K_h, "i":K_i, "j":K_j, "l":K_l, "m":K_m, 
	"n":K_n, "o":K_o, "p":K_p, "q":K_q,	"r":K_r, "s":K_s, "t":K_t, "u":K_u, "v":K_v, "w":K_w, "x":K_x, "z":K_z	
}

ACTION_MAP = {
	"move left":move_left, "move right":move_right, "move up": move_up, "move down":move_down,
	"jump":move_jump, "sprint":move_sprint,
	"melee attack":melee_attack, "ranged attack":ranged_attack, "interact":interact, "pause":press_return, "inventory":open_inventory, "map":open_map,
	"toggle lantern left":press_q, "toggle lantern right":press_w, "lantern ability":press_c
}