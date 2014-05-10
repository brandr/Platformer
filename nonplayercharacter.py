""" A non-hostile character that the player can walk past and not bounce off of.
"""

from being import *
from gameevent import *
from dialogchoice import *

class NonPlayerCharacter(Being):
	""" TODO: docstring
	"""
	def __init__(self, animations, x, y):#, portrait_set_key = None):
		Being.__init__(self, animations, x, y)
		self.animated = True
		self.up_interactable = True
		self.scrolling = True #might want to make more elaborate scrolling later
		self.name = None

		#TEMPORARY FOR TESTING

		self.start_dialog = None

		one_pane_dialog_tree = (
									[
										("Whaaaaaaaaaaat is this place?? \n" + "It looks like some kind of... demo.", NEUTRAL)
									], None
								)
		two_pane_dialog_tree = (
									[
										("Whaaaaaaaaaaat is this place?? \n" + "It looks like some kind of... demo.", NEUTRAL),
										("Do you know the way out of here?", NEUTRAL)
									], None
								)

		#TODO: redesign this structure so that lists of dialogs can be paired not only to dialog choices or None, but also to miscellaneous actions
		# use string keys or something
		self.dialog_tree = (
									[
										("Whaaaaaaaaaaat is this place??", NEUTRAL),
										("It looks like some kind of... demo.", NEUTRAL)
									],
									(
										("Do you know the way out of here?", NEUTRAL),
										[ 
											("Yes", 
												[
													("I don't believe you!", NEUTRAL)
												], None
											),
											("No", 
												[
													("Well, let me know if you find it.", NEUTRAL)
												], None
											)
										]
									)
							)

		#self.init_dialogs(dialog_tree)

	def init_dialogs(self, dialog_tree):
		start_dialog_set = self.build_dialog_set(dialog_tree[0])
		start_choice_data = dialog_tree[1]
		if(start_choice_data):	#TODO: case for next action that is not just the end of the conversation. (maybe use constant keys?)
			start_choice_text_data = start_choice_data[0]
			start_choice_list = start_choice_data[1]
			portrait_filename = self.build_portrait_filename(start_choice_text_data[1])
			start_dialog_choice = DialogChoice(self, SIGN, start_choice_list, start_choice_text_data[0], portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling)
			start_dialog_set[-1].add_next_action(start_dialog_choice)
			#TODO: recursion? (or handle the rest of what needs to be done is the DialogCHoice class)
		#else:
		#	pass #TODO
		self.first_dialog = start_dialog_set[0]

	def build_dialog_set(self, dialog_data):
		dialog_set = []
		for d in dialog_data:
				portrait_filename = self.build_portrait_filename(d[1])
				dialog = Dialog(SIGN, d[0], portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling) 
				dialog_set.append(dialog)
		for i in range(0, len(dialog_set) - 1):
			dialog_set[i].add_next_action(dialog_set[i + 1])
		return dialog_set

	def execute_event(self, level):
		# TODO: Probably allow non-linear dialogue by implementing a "DialogTree" class with nodes that hold the data needed to create
		# dialogs and a reliable way to check whether each node has a y/n question or not.
		#if self.text_set:
		#	dialog_set = []
		#	for t in self.text_set:
		#		portrait_filename = self.portrait_filename(t[1])
		#		dialog = Dialog(t[0], portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling) 
		#		dialog_set.append(dialog)
		#	for i in range(0, len(dialog_set) - 1):
		#		#TODO: the "next action" may be determined by how the player answers a yes/no question.
		#		dialog_set[i].add_next_action(dialog_set[i + 1])
		self.init_dialogs(self.dialog_tree)
		event = GameEvent([self.first_dialog])
		event.execute(level) #NOTE: be careful about the tabbing of this line!

	def build_portrait_filename(self, key):
		if self.name == None:
			return None
		return "portrait_" + self.name + "_" + key + ".bmp"

NEUTRAL = "neutral"

NPCS_WITH_PORTRAITS = ["Kenstar"] #TODO: if this NPC's name is in this list, they have a portrait. Otherwise, they don't.
								  # might not need this: could just use a default (None) arg for all NPCs that don't have portraits.

#KENSTAR_PORTRAIT_SET = {} #TODO: instead of mapping individual key words to portrait filenames, build the filenames out of their individual components