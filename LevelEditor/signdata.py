""" A special kind of tiledata specific to signs"""

from tiledata import *

class SignData(TileData):
	""" TODO: docstring"""
	def __init__(self, key, filepath, filepath_start = "./"):
		TileData.__init__(self, key, filepath, filepath_start)
		#TODO: we also need data to represent the sign's text
		#self.temp_data = "check dis data bro"	
		self.text_panes = [
			["", "", "", ""]
		]

	def create_copy(self):
		copy_sign = SignData(self.entity_key, self.image_filepath)
		copy_sign.text_panes = self.text_panes
		return copy_sign

	def set_sign_text(self, text_panes):
		self.text_panes = text_panes

	def formatted_data(self):
		return (self.entity_key, self.image_filepath, self.width, self.height, self.text_panes) 