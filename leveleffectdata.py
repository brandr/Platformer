""" A special kind of tiledata specific to level effects"""

from tiledata import *

class LevelEffectData(TileData):
	""" LevelEffectData( str, str, str ) -> LevelEffectData

	A special type of tiledata used to generate level effects.

	Attrbitues:

	TODO
	"""

	def __init__(self, key, filepath, filepath_start = "./"):
		TileData.__init__(self, key, filepath, filepath_start)
		#TODO: additional information goes here

	def create_copy(self):
		copy_effect = LevelEffectData(self.entity_key, self.image_filepath)
		#TODO: additional information goes here
		return copy_effect

	def formatted_data(self):
		""" cd.formatted_data( ) -> ( str, str, int, int )

		Format this leveleffectdata into primitive types so that it can be saved to a file.
		"""
		return (self.entity_key, self.image_filepath, self.width, self.height) #TODO: add additional information

	def get_image(self, filepath_start = "./"):	#TODO: consider allowing filepath beginning here.
		filename = "./images/" + self.image_filepath.split("/")[-1]
		return TileData.load_image(filename)
		#filepath = filepath_start + self.image_filepath
		#image = TileData.load_image(filepath)
		#image.set_colorkey(DEFAULT_COLORKEY)
		#return image