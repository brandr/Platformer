""" A specific type of dialog to be used when the player is given a dialog choice.
"""

from dialog import *

UP, DOWN = "up", "down"

class DialogChoice(Dialog):
	""" TODO: docstring
	"""

	def __init__(self, source, source_group, choice_data_list, text = "", portrait_filename = None, dimensions = (0, 0), scrolling = False, font_color = BLACK):
		self.choice_data_list = choice_data_list
		self.source = source
		for d in self.choice_data_list:
			#choice_text, choice_set, choice_next_action = d[0], d[1], d[2]
			choice_text = d[0]
			text += "\n" + choice_text
			#TODO
		self.choosing = False
		self.select_index = 0
		Dialog.__init__(self, source_group, text, portrait_filename, dimensions, scrolling, font_color)

	def current_choice(self):
		return self.choice_data_list[self.select_index]

		# EXAMPLE of choice_data:
		#yn_choices = [("Yes", yes_text_set, None), ("No", no_text_set, None)] 

	def process_key(self, key):
		if(self.index/SCROLL_CONSTANT >= len(self.text)):
			if(key == UP):
				self.select_index = max(0, self.select_index - 1)
			elif(key == DOWN):
				self.select_index = min(len(self.choice_data_list) - 1, self.select_index + 1)
	
	def draw_text_image(self):
		text_image = Dialog.draw_text_image(self)
		if(self.index/SCROLL_CONSTANT >= len(self.text)):
			arrow = Surface((12, 12)) #TEMP
			text_image.blit(arrow, (4, 8 + 32 * (1 + self.select_index))) #TEMP VALUES
			#TODO: draw arrow pointing to currently selected option (currently just a black square)
		return text_image

	#def execute_event(self, level):
	#	print "HERE"

	def update(self):
		Dialog.update(self)
		if(self.index/SCROLL_CONSTANT >= len(self.text)):
			self.choosing = True
		
	def continue_action(self, event, level):
		if(self.index/SCROLL_CONSTANT <= len(self.text)):
			self.index = int(SCROLL_CONSTANT * len(self.text))
			return True
		event.remove_action(self)
		level.remove_effect(self)

		choice = self.current_choice()
		dialog_branch = self.build_dialog_branch(choice[1])
		next_action = choice[2] #not sure this is what we want yet, nor where to use it
		if(next_action != None):
			dialog_branch[-1].add_next_action(next_action)
		event.add_action(dialog_branch[0])
		dialog_branch[0].execute(level)
		return True
		#TODO: make this work if there are next actions other than None (including additional choices)

	def build_dialog_branch(self, dialog_data):
		dialog_set = []
		for d in dialog_data:
				portrait_filename = self.build_portrait_filename(d[1])
				dialog = Dialog(SIGN, d[0], portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling) #SIGN arg is temporary
				dialog_set.append(dialog)
		for i in range(0, len(dialog_set) - 1):
			dialog_set[i].add_next_action(dialog_set[i + 1])
		return dialog_set

	def build_portrait_filename(self, key):
		if self.source.name == None:
			return None
		return "portrait_" + self.source.name + "_" + key + ".bmp"

	#def continue_action(self, event, level):
	#	print "HERE"
	#	Dialog.continue_action(self, event, level)