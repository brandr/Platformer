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

		self.right = False #TEMP

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
		branching_dialog_tree = (
									[
										("Whaaaaaaaaaaat is this place??", NEUTRAL),
										("It looks like some kind of... demo.", NEUTRAL)
									],
									(
										DIALOG_CHOICE,
										("Do you know the way out of here?", NEUTRAL),
										[ 
											("Yes", 
												[
													("Whoa, really?", NEUTRAL)
												],
												(
													DIALOG_CHOICE,
													("Is it to the right?", NEUTRAL),
													[
														("Yes",
															[
																("Well, then, I'd better get going!", NEUTRAL),
																("...and by that, I mean walk slightly to the right.", NEUTRAL)		
															],

															(
																ACTION_SET,
																[ 
																	(	#TODO: make the action work
																		NonPlayerCharacter.temp_npc_right_method, 20, None 
																	),
																	(
																		NonPlayerCharacter.temp_stop_method, 0, None 
																	)
																]
															)
														),
														("No",
															[
																("I don't belive you! I came from that direction!", NEUTRAL)
															], None
														)
													]
												)
											),
											("No", 
												[
													("Well, let me know if you find it.", NEUTRAL)
												], None
											)
										]
									)
							)

		linear_action_tree = (
								[
									("Whaaaaaaaaaaat is this place?? \n" + "It looks like some kind of... demo.", NEUTRAL),
									("I'd bettter go look for Yusuke...", NEUTRAL),
									("...and by that, I mean walk slightly to the right.", NEUTRAL)
								], 	
								( #TODO: create a framework for "next action" that works for choice dialogs and other actions alike
								  #TODO: change the framework so that multiple actions can be executed in turn (this will be useful for
								  # making a character stop after walking a certain distance)

									ACTION_SET,
									[ 
										(
											NonPlayerCharacter.temp_npc_right_method, 20, None 
										),
										(
											NonPlayerCharacter.temp_stop_method, 0, None 
										)
									]
									#GameAction(NonPlayerCharacter.temp_npc_right_method, 60, None, self)
								)
							)

		self.dialog_tree = branching_dialog_tree #branching_dialog_tree
		#TODO: make it so talking to a character multiple times can (but doesn't always) yield different results.
		# think of some example structures before implementing this
		# for instance, should there be a "default" response that the character resolves into?
		# How should y/n interactions affect the "next" dialog tree?

	def get_name(self):
		return self.name

	def get_source(self): #get_source is used to make dialog trees work properly.
		return self

	def update(self, player):
		#TEMP	
		if(self.right):
			self.xvel = 4
			self.direction_id = 'right'	
			self.changeAnimation('idle', self.direction_id)
		else:
			self.xvel = 0
		#TEMP	

		Being.update(self, player)
		Being.updatePosition(self)

	def temp_stop_method(self, arg = None):
		self.left, self.right, self.up, self.down = False, False, False, False	

	def temp_npc_right_method(self, arg = None): #TEMP for testing
		self.right = True

	def init_dialogs(self, dialog_tree):
		full_dialog_set = None
		start_dialog_set = self.build_dialog_set(dialog_tree[0])
		start_action_data = dialog_tree[1]
		if(start_action_data):
			full_dialog_set = self.init_dialog_set(start_dialog_set, start_action_data)	
		self.first_dialog = full_dialog_set[0]

	def init_dialog_set(self, dialog_set, action_data):
		action_key = action_data[0]
		build_method = BUILD_METHOD_MAP[action_key]
		return build_method(self, dialog_set, action_data)

	def build_dialog_choice_set(self, dialog_set, action_data):
		start_choice_text_data = action_data[1]
		start_choice_list = action_data[2]
		portrait_filename = self.build_portrait_filename(start_choice_text_data[1])
		start_dialog_choice = DialogChoice(self, SIGN, start_choice_list, start_choice_text_data[0], portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling)
		#TODO: fix the SIGN part (probably by getting some key associated with NPCs)
		dialog_set[-1].add_next_action(start_dialog_choice)
		return dialog_set

	def build_action_set(self, dialog_set, action_data):
		action_data_set = action_data[1]
		action_set = []
		for a in action_data_set:
			action = GameAction(a[0], a[1], self, a[2])
			action_set.append(action)
		for i in range(0, len(action_data_set) - 1):
			action_set[i].add_next_action(action_set[i + 1])
		dialog_set[-1].add_next_action(action_set[0])
		return dialog_set

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

DIALOG_CHOICE = "dialog_choice"
ACTION_SET = "action_set"	#consider other data types
BUILD_METHOD_MAP = {
	DIALOG_CHOICE:NonPlayerCharacter.build_dialog_choice_set, 
	ACTION_SET:NonPlayerCharacter.build_action_set
	}