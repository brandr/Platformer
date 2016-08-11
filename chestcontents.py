""" Data relates to chest contents are stored in this file.
"""

from lantern import Lantern
from meleeweapon import MeleeWeapon

# item constants
ITEM_CLASS = "item_class"
ITEM_KEY = "item_key"
DISPLAY_NAME = "display_name"
RECEIVE_DIALOG_DATA = "receieve_dialog_data"
#TODO: other constants

LANTERN_MAP = {
	ITEM_CLASS:Lantern, 
	ITEM_KEY:"lantern",
	DISPLAY_NAME: "Lantern",
	RECEIVE_DIALOG_DATA:
	[
		[
			"You got a lantern!",
			"It will light up when you travel through dark places.",
			"Using it will drain your lantern oil."
		]
	]
}

SWORD_MAP = {
	ITEM_CLASS:MeleeWeapon, 
	ITEM_KEY:"sword",
	DISPLAY_NAME: "Sword",
	RECEIVE_DIALOG_DATA:
	[
		[
			"You got a sword! Swing it with Z!",
			"Be careful! You could poke an eye out!"
		]
	]
}

SUBENTITY_LIST = ["sword"]

MASTER_CHEST_CONTENTS_MAP = {
	"lantern":LANTERN_MAP,
	"sword":SWORD_MAP
}