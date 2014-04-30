""" A cutscene during which things happen and buttons only advance the dialog.
"""

from gameevent import *

class Cutscene(GameEvent):
	""" TODO: docstring
	"""
	def __init__(self, actors): #TODO
		GameEvent.__init__(self)
		self.actors = actors

		self.duration = 20 #TEMP. Later, we want to give each action in the cutscene a duration instead.

	def begin(self):
		self.actors[0].right = True #TEMP. Make this more general, and also make it possible for the cutscene to progress/end.

	def update(self):
		self.duration -= 1 #TEMP.

	def is_complete(self):
		return self.duration <= 0 #TEMP