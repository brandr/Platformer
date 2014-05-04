""" A scripted game event, like a sign displaying text or a cutscene.
"""

from dialog import *
from gameaction import *

# IDEA: make  a gameevent instant only

class GameEvent:
	def __init__(self, start_actions = []): #TEMP
		self.current_actions = start_actions
		self.level = None

	def execute(self, level):
		self.level = level
		level.begin_event(self)
		for a in self.current_actions:
			a.execute(level)
		#TODO: if self.actions, execute all starting actions 
		#if self.actions:
		#	self.current_action = self.actions[0] #TODO: actually begin the action
		#level.display_dialog(self.current_dialog)

	def continue_event(self):
		if self.current_actions:
			should_continue = False
			for a in reversed(self.current_actions):
				if a.continue_action(self, self.level):
					should_continue = True
			return should_continue
		#NOTE: this is not a constant update method, but is called when the player presses X.
		# 	   it's possible that other keys should be allowed to pass into an event. Might make a key dict for some situations.
		return False 

	def add_action(self, action):
		self.current_actions.append(action)

	def remove_action(self, event):
		self.current_actions.remove(event)

	def update(self):
		for a in self.current_actions:
			a.update()
		#pass
			#TODO (or maybe have subclasses inherit). Should probably update all current actions, which will
			# add new actions to this event if necessary. Finished actions are removed.
			# should iterate in reverse so that removing actions does not mess up the updating process.

	def is_complete(self):
		return not self.current_actions #TEMP