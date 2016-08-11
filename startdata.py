from inventory import Inventory
from chestcontents import *
from itemfactory import build_item

class StartData(object):
	""" StartData( ( String, ( int, int ) ), PlayerData ) -> StartData

	Data used when loading a saved game.

	Attributes:

	start_level_key, start_x, start_y: Show the location where the player saved.

	player_data: data specific to the player, such as the player's inventory.
	"""
	def __init__(self, level_key, start_pos, player_data):
		self.start_level_key = level_key
		self.start_x = start_pos[0]
		self.start_y = start_pos[1]
		self.player_data = player_data

	def load_inventory(self):
		""" def load_inventory( ) -> inventory

		Load the inventory that the player should start with.
		"""
		inventory = Inventory()
		for i in self.player_data.inventory_data:
			constructor = MASTER_CHEST_CONTENTS_MAP[i][ITEM_CLASS]
			item = build_item(constructor, i, 0, 0)
			inventory.add_item(item, i)
		return inventory