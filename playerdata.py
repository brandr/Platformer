class PlayerData(object):
	""" PlayerData( Player ) -> PlayerData

	An object used to keep track of information about the player when saving the game.

	Attributes:

	inventory_data: a list of item keys that will be used to load the player's inventory.
	"""
	def __init__(self, inventory):
		self.load_inventory_data(inventory)
		#self.load_meter_data(player)

	def load_inventory_data(self, inventory):
		""" load_inventory_data( Inventory ) -> None

		Set up the list of all item keys for this playerdata object.
		"""
		self.inventory_data = []
		for k in inventory.get_all_item_keys():
			self.inventory_data.append(k)

	def load_meter_data(self, player):
		""" load_meter_data( Player ) -> None

		Set up all meters (such as lantern oil).
		"""
		self.meter_amounts = {}
		lantern = player.get_lantern()
		if(lantern): self.meter_amounts["lantern"] = lantern.oil_meter

	def load_formatted_meter_data(self, formatted_data):
		""" load_formatted_meter_data( self, ( String, [ int, int ] ) ) -> None

		Sets up meter data using formatted data rather than the player.
		"""
		self.meter_amounts = {}
		for d in formatted_data:
			self.meter_amounts[d[0]] = d[1]

	def formatted_data(self):
		""" formatted_data( ) -> ( [ String ] )

		Format PlayerData so it can be saved to a file.
		"""
		meter_data = []
		for k in METER_KEYS:
			if k not in self.meter_amounts: continue 
			meter_amount = self.meter_amounts[k]
			meter_data.append(( k, meter_amount ))
		return (self.inventory_data, meter_data)	#TODO: other player data, such as lantern oil amount and morality

METER_KEYS = ["lantern"]