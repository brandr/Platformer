""" A special kind of tiledata specific to chests"""

from tiledata import *

class ChestData(TileData):
	""" ChestData( str, str, str ) -> ChestData

	A special type of tiledata used to generate chests.

	Attrbitues:

	contents_key: Used to figure out what item is in the chest.
	"""

	def __init__(self, key, filepath, filepath_start = "./"):
		TileData.__init__(self, key, filepath, filepath_start)
		self.contents_key = None

	def create_copy(self):
		copy_chest = ChestData(self.entity_key, self.image_filepath)
		copy_chest.contents_key = self.contents_key #TEMP
		return copy_chest

	def formatted_data(self):
		""" cd.formatted_data( ) -> ( str, str, int, int, str )

		Format this chestdata into primitive types so that it can be saved to a file.
		"""
		return (self.entity_key, self.image_filepath, self.width, self.height, self.contents_key) #TODO: add contained item 