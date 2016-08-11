from entity import Entity
from gameevent import GameEvent
from dialog import Dialog, SIGN
from dialogchoice import DialogChoice, ACTION_SET
from startdata import StartData
from sign import DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT
from pygame import Rect

import json
from json import *
from os import path

DEFAULT_SAVE_TEXT = "Would you like to save?"


class SavePoint(Entity):
	""" SavePoint( AnimationSet, int, int ) -> SavePoint

	A SavePoint is a special entity that allows the player to save the game.
	It will probably be easiest to make it work similarly to an NPC or a sign, since it will open a dialog

	Attributes:

	"""
	def __init__(self, animations, x, y):
		Entity.__init__(self, animations)
		self.rect = Rect(x, y, 32, 32)
		self.x_interactable = True
		self.scrolling = True

	def get_source(self):
		""" sp.get_source( ) -> SavePoint

		A general method used to make dialog trees work properly whether the source of the dialog is an NPC, a sign, or a save point.
		"""
		return self

	def build_save_event(self):
		""" sp.build_save_event() -> GameEvent

		Returns a GameEvent containing this save point's save dialog.
		"""
		dialog = DialogChoice(self, SIGN, DEFAULT_SAVE_CHOICE_DATA_LIST, DEFAULT_SAVE_TEXT, None, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling)
		return GameEvent([dialog])

	def execute_x_action(self, level, player):
		""" sp.execute_x_action( Level, Player ) -> None

		This is called when the player presses X near the save point.
		This causes the sign's dialog box to appear.
		"""
		save_event = self.build_save_event()
		save_event.execute(level)

	def save_game(self, arg = None):
		""" sp.save_game( None ) -> None

		Save the game. Expand on this docstring as it gets more complex.
		"""
		#TODO: make the game save everything that it should. Need to add:
		# - player map
		# - opened chests (this falls under "change data" or whatever I was planning to call it)
		# - some (but not all) destroyed blocks (need the blocks' original locations)
		# these things can go in "start data".
		level = self.current_level
		dungeon = level.dungeon
		player = level.getPlayer()
		dungeon_data = dungeon.dungeon_build_data
		filename = dungeon.filename
		level_name = self.current_level.level_ID
		x = player.rect.left
		y = player.rect.top
		player_data = player.player_data()
		formatted_player_data = player_data.formatted_data()
		#TODO: include formatted "change data" in the formatted start data here.
		formatted_start_data = (level_name, (x, y), player_data.formatted_data())
		formatted_data = dungeon_data.formatted_data()
		save_data = (formatted_data[0], formatted_data[1], formatted_start_data)
		filepath = "./saves/" + filename
		dungeon_file = open(filepath, 'wb') #'wb' means "write binary"
		json.dump(save_data, dungeon_file)

DEFAULT_SAVE_CHOICE_DATA_LIST = [
	("Yes", [], 
		(
			ACTION_SET,
			[
				(
					SavePoint.save_game, 1, None
				)
			],
		)
	),
	("No", [], None)
]
