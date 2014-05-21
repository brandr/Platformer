""" A special pane used in the LevelEditor fuor some (but not all) entity types to specify additional data.
"""

from ocempgui.widgets import Bin, Box, FileList, Label, ImageLabel, Label, Entry, Button
from ocempgui.widgets.BaseWidget import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

class EntityDataPane(Box): #TODO: figure what class this should extend
	"""TODO: docstring"""
	def __init__(self, width, height):
		Box.__init__(self, width, height)
		self.update_empty()
		self.current_selection = None
		self.additional_data = None

	def select_tile(self, tile_data):
		entity_key = tile_data.entity_key #TODO: update self.current_selection if necessary
		self.update_data(entity_key, tile_data)

	def deselect_tile(self):
		self.current_selection = None
		self.additional_data = None
		self.update_empty()

	def update_data(self, entity_key, entity_data):
		if entity_key in ENTITY_DATA_MAP:
			self.current_selection = entity_data
			update_method = ENTITY_DATA_MAP[entity_key]
			update_method(self)
		else:
			self.update_empty()

	def update_empty(self):
		data_label = Label("No additional data.")
		self.set_children([data_label])

	def update_sign(self):
		sign_data = self.current_selection
		#TODO: allow saving sign text so that it corresponds to sign_data (a specific TileData object)
			# - not sure if this alone will make it possible to give different signs different text or not
		#TODO: add buttons which allow scrolling through different panes of sign text.
			# -also allow adding panes (in a different, distinct way)
		#TODO: modify TileData reading so that a sign can be created in the leveleditor, have its text panes set, and then
			#  added to the game with the same text panes.

		#print sign_data.temp_data #TEST

		sign_label = Label("Sign Text:")
		sign_text_panes = sign_data.text_panes
		sign_text_entries = []

		for i in range(0, 1): #TEMP: want to iterate through all panes eventually
			sign_text_lines = sign_text_panes[i]
			y_offset = 16
			for s in sign_text_lines:
				next_entry = Entry(s)
				next_entry.set_minimum_size(self.width, 12)
				next_entry.padding = 4
				next_entry.top += y_offset
				y_offset += 24
				sign_text_entries.append(next_entry)

		self.set_children([sign_label])	#TEMP: want to iterate through all panes eventually (and only add children for 0, or )
		for s in sign_text_entries:
			self.add_child(s)

		self.sign_entry_set = sign_text_entries #TEMP. eventually I want to replace this with the set of all panes.
		bottom_entry = sign_text_entries[-1]
		save_sign_button = self.save_sign_button(bottom_entry.left, bottom_entry.bottom + 8)
		self.add_child(save_sign_button)

	def save_sign_button(self, x, y):
		button = Button("Save sign text")
		button.topleft = x, y
		button.connect_signal(SIG_CLICKED, self.save_sign_data)	
		return button

	def save_sign_data(self):
		sign_text_panes = []
		for i in range(0, 1): #TEMP: eventually want to get all panes
			sign_text_panes.append([])
			for j in range(0, 4):
				next_entry = self.sign_entry_set[j]
				next_text = next_entry.text	
				sign_text_panes[i].append(next_text)
		self.current_selection.set_sign_text(sign_text_panes)
		 #TODO: change self.current_selection on the assumption that it is a SignData object (set the text panes)

DEFAULT_SIGN = "default_sign"
ENTITY_DATA_MAP = {
		DEFAULT_SIGN:EntityDataPane.update_sign #TODO
}