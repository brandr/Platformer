""" A non-hostile character that the player can walk past and not bounce off of.
"""

from being import *
from gameevent import *
from dialogchoice import *

class NonPlayerCharacter(Being):
	""" TODO: docstring
	"""
	def __init__(self, animations, x, y):
		Being.__init__(self, animations, x, y)
		self.animated = True
		self.x_interactable = True
		self.scrolling = True #might want to make more elaborate scrolling later
		self.name = None
		self.active = True
		self.direction_id = 'left'
		self.changeAnimation('idle','left')

		self.right = False #TEMP

	def get_name(self):
		return self.name

	def get_source(self): # get_source is used to make dialog trees work properly.
		return self

	def update(self, player):
		self.changeAnimation('idle', self.direction_id)
		if self.active:
			self.NPC_update(player)
		#TEMP	
		if(self.right):
			self.xvel = 4
			self.direction_id = 'right'	
		else:
			self.xvel = 0
		#TEMP	

		Being.update(self, player)
		Being.updatePosition(self)

	def NPC_update(self, player):	#NOTE: might want some NPCs to walk around instead of doing this. Not sure.
		self.face_towards(player)

	def face_towards(self, target):
		if(target != None):
			x_dist = target.coordinates()[0] - self.current_tile().coordinates()[0]
			if x_dist == 0: return
			self.direction_val = x_dist/abs(x_dist)
			if self.direction_val == -1:
				self.direction_id = 'left'
			if self.direction_val == 1:
				self.direction_id = 'right'

	def set_active(self, active):
		self.active = active

	def temp_stop_method(self, arg = None):
		self.left, self.right, self.up, self.down = False, False, False, False	

	def temp_npc_right_method(self, arg = None): #TEMP for testing
		self.right = True

	def init_dialogs(self, dialog_tree):
		start_dialog_set = self.build_dialog_set(dialog_tree[0])
		start_action_data = dialog_tree[1]
		if(start_action_data):
			start_dialog_set = self.init_dialog_set(start_dialog_set, start_action_data)	
		self.first_dialog = start_dialog_set[0]

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

	def add_dialog_set(self, start_dialog_set, add_dialog_data):
		next_dialog_data = add_dialog_data[1]
		next_dialog_set = self.build_dialog_set(next_dialog_data)
		next_action_data = add_dialog_data[2]
		if(next_action_data):
			next_dialog_set = self.init_dialog_set(next_dialog_set, next_action_data)
		start_dialog_set[-1].add_next_action(next_dialog_set[0])
		return start_dialog_set

	def build_action_set(self, dialog_set, action_data):
		action_data_set = action_data[1]
		action_set = []
		for a in action_data_set:
			action = GameAction(a[0], a[1], self, a[2])
			action_set.append(action)
		for i in range(0, len(action_data_set) - 1):
			action_set[i].add_next_action(action_set[i + 1])
		dialog_set[-1].add_next_action(action_set[0])
		next_action_data = action_data[2]  #this part is untested and may cause bugs.
		if next_action_data:
			dialog_set = self.init_dialog_set(action_set, next_action_data)
		return dialog_set

	def setup_next_dialog(self, dialog_set, action_data):	#no need to check for next action because this is done at the very end only.
		dialog_key = action_data[1]
		action = GameAction(NonPlayerCharacter.change_current_dialog, 0, self, dialog_key)
		dialog_set[-1].add_next_action(action)
		return dialog_set

	def change_current_dialog(self, dialog_key):
		self.dialog_tree = self.dialog_tree_map[dialog_key] #might want error checking here

	def build_dialog_set(self, dialog_data):
		dialog_set = []
		for d in dialog_data:
				portrait_filename = self.build_portrait_filename(d[1])
				dialog = Dialog(SIGN, d[0], portrait_filename, (DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT), self.scrolling) #TODO: change the SIGN arg
				dialog_set.append(dialog)
		for i in range(0, len(dialog_set) - 1):
			dialog_set[i].add_next_action(dialog_set[i + 1])
		return dialog_set
		
	def execute_x_action(self, level, player):
		self.execute_event(level)

	def execute_event(self, level):
		self.init_dialogs(self.dialog_tree)
		event = GameEvent([self.first_dialog])
		event.execute(level)

	def build_portrait_filename(self, key):
		if self.name == None:
			return None
		return "portrait_" + self.name + "_" + key + ".bmp"

NEUTRAL = "neutral"

KENSTAR = "kenstar"

#NPCS_WITH_PORTRAITS = ["Kenstar"] #TODO: if this NPC's name is in this list, they have a portrait. Otherwise, they don't.
								  # might not need this: could just use a default (None) arg for all NPCs that don't have portraits.

#KENSTAR_PORTRAIT_SET = {} #TODO: instead of mapping individual key words to portrait filenames, build the filenames out of their individual components

ACTION_SET = "action_set"	
ADD_DIALOG_SET = "add_dialog_set"
DIALOG_CHOICE = "dialog_choice"
SETUP_NEXT_DIALOG = "setup_next_dialog"
BUILD_METHOD_MAP = {
	ACTION_SET:NonPlayerCharacter.build_action_set,
	ADD_DIALOG_SET:NonPlayerCharacter.add_dialog_set,
	DIALOG_CHOICE:NonPlayerCharacter.build_dialog_choice_set, 
	SETUP_NEXT_DIALOG:NonPlayerCharacter.setup_next_dialog
}