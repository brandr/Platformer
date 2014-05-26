""" A sign that the player can read. No one else can, though.
"""

from block import *
from gameevent import *

DIALOG_BOX_WIDTH = WIN_WIDTH - 32
DIALOG_BOX_HEIGHT = WIN_HEIGHT/6

class Sign(Block): #TODO: figure out how to set text, # of panes, whether text is scrolling, etc.
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.up_interactable = True
		self.scrolling = True #might want to make more elaborate scrolling later
		self.text_set = None
		self.is_solid = False

	def set_text_set(self, text_set):
		self.text_set = []
		for i in xrange(len(text_set)):
			self.text_set.append("")
			for line in text_set[i]:
				if line != "":
					self.text_set[i] += line + "\n"
		#self.text_set = text_set
	
	def execute_event(self, level):
		if self.text_set:
			dialog_set = self.build_dialog_set(self.text_set)
			event = GameEvent([dialog_set[0]])
			event.execute(level)

	def build_dialog_set(self, text_data):
		dialog_set = []
		for t in text_data:
				#portrait_filename = self.build_portrait_filename(d[1])
				dialog = Dialog(SIGN, t, None, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling)
				dialog_set.append(dialog)
		for i in range(0, len(dialog_set) - 1):
			dialog_set[i].add_next_action(dialog_set[i + 1])
		return dialog_set