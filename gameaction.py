""" An action in the game which has another action after it.
Spefically meant for cutscenes.
"""

class GameAction:
	""" TODO: docstring
	"""
	def __init__(self, method, duration = 0, actor = None, arg = None):
		self.next_actions = []
		self.method = method
		self.duration = duration
		self.actor = actor
		self.arg = arg

	def add_next_action(self, action):
		self.next_actions.append(action)

	def continue_action(self):
		return False #TODO: may need a better way to determine this

	def execute(self, level):
		self.method(self.actor, self.arg)

	def update(self, event):
		if self.duration <= 0:
			event.remove_action(self)
			return
		self.duration -= 1