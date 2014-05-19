""" A factory for adding text to signs.
"""

from sign import *

class SignFactory:
	""" TODO: docstring
	"""
	@staticmethod
	def init_sign(sign, sign_key):	#not sure if I can use sign_key-- might need a different structure to figure out the proper text
		sign.set_text_set(TEST_SIGN_TEXT_SET)	#TEMP

TEST_SIGN_TEXT_SET = [
	"This is a sign. Press X to advance the dialog box.",
	"This is the only thing any sign can ever say."
]