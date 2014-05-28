""" A factory for adding text to signs.
"""

from sign import *

class SignFactory:
	""" TODO: docstring
	"""
	@staticmethod
	def build_entity(raw_sign_image, sign_rect, sign_data, x, y):	#not sure if I can use sign_key-- might need a different structure to figure out the proper text
		still_entity_image = GameImage.still_animation_set(raw_sign_image, sign_rect)
		sign = Sign(still_entity_image, x, y)
		sign_text_panes = sign_data.text_panes
		sign.set_text_set(sign_text_panes)
		return sign