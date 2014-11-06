""" An inventory of items held by the player.
"""

LANTERN = "lantern"

class Inventory:
	""" Inventory( ) -> Inventory

	By default, an inventory is generated empty, but items can be added to it.
	"""
	def __init__(self):
		self.items = {}
		#self.lantern = None
		#TODO

	def add_item(self, item, key):
		""" l.add_item( Item, str ) -> None

		Add an item to this inventory by first checking what item it is, then pmapping it to the given key.
		"""
		self.items[key] = item

	def get_item(self, key):
		""" l.get_item( str ) -> Item

		Find the item using the key.
		"""
		if not key in self.items: return None
		return self.items[ key ]