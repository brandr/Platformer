""" A non-hostile character that the player can walk past and not bounce off of.
"""

from being import *
from gameevent import *

DIALOG_BOX_WIDTH = WIN_WIDTH - 32
DIALOG_BOX_HEIGHT = WIN_HEIGHT/6

class NonPlayerCharacter(Being):
	""" TODO: docstring
	"""
	def __init__(self, animations, x, y):
		Being.__init__(self, animations, x, y)
		self.animated = True
		self.up_interactable = True
		self.scrolling = True #might want to make more elaborate scrolling later

		#TEMPORARY FOR TESTING

		text_1 = "Whaaaaaaaaaaat is this place??"
		#text_2 = "This is the only thing any sign can ever say."
		self.text_set = [text_1]

	def execute_event(self, level):
		if self.text_set:
			dialog_set = []
			for t in self.text_set:
				dialog = Dialog(SIGN, t, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling) #TODO: change sign arg to something else
				dialog_set.append(dialog)
			for i in range(0, len(dialog_set) - 1):
				dialog_set[i].add_next_action(dialog_set[i + 1])
			event = GameEvent([dialog_set[0]])
			event.execute(level)