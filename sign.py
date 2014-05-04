""" A sign that the player can read. No one else can, though.
"""

from block import *
from gameevent import *

SIGN_WIDTH = WIN_WIDTH - 32
SIGN_HEIGHT = WIN_HEIGHT/6

class Sign(Block): #TODO: figure out how to set text, # of panes, whether text is scrolling, etc.
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.scrolling = True #might want to make more elaborate scrolling later
		text_1 = "This is a sign. Press X to advance the dialog box."
		text_2 = "This is the only thing any sign can ever say."
		self.text_set = [text_1, text_2]
	
	def execute_event(self, level):
		if self.text_set:
			dialog_set = []
			for t in self.text_set:
				dialog = Dialog(SIGN, t, (SIGN_WIDTH, SIGN_HEIGHT), self.scrolling)
				dialog_set.append(dialog)
			for i in range(0, len(dialog_set) - 1):
				dialog_set[i].add_next_action(dialog_set[i + 1])
			event = GameEvent([dialog_set[0]])
			event.execute(level)