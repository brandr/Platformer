""" A special kind of tiledata specific to level effects"""

from tiledata import *
import pygame
from pygame import Color

DEFAULT_COLORKEY = Color(("#FF00FF"))

class LevelEffectData(TileData):
	""" LevelEffectData( str, str, str ) -> LevelEffectData

	A special type of tiledata used to generate level effects.

	Attrbitues:

	TODO
	"""

	def __init__(self, key, filepath, filepath_start = "./"):
		TileData.__init__(self, key, filepath, filepath_start)
		self.transparency = 255

	def create_copy(self):
		copy_effect = LevelEffectData(self.entity_key, self.image_filepath)
		copy_effect.transparency = self.transparency
		return copy_effect

	def formatted_data(self):
		""" cd.formatted_data( ) -> ( str, str, int, int )

		Format this leveleffectdata into primitive types so that it can be saved to a file.
		"""
		return (self.entity_key, self.image_filepath, self.width, self.height, self.transparency)

	def get_image(self, filepath_start = "./"):	#TODO: consider allowing filepath beginning here.
		filepath = filepath_start + self.image_filepath
		image = TileData.load_image(filepath)
		image.set_colorkey(DEFAULT_COLORKEY)
		return image