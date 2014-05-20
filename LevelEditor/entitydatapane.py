""" A special pane used in the LevelEditor fuor some (but not all) entity types to specify additional data.
"""

from ocempgui.widgets import Bin, Box, FileList, Label, ImageLabel, Label, Entry
from ocempgui.widgets.BaseWidget import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

class EntityDataPane(Box): #TODO: figure what class this should extend
	"""TODO: docstring"""
	def __init__(self, width, height):
		Box.__init__(self, width, height)
		self.update_empty()
		self.current_selection = None

	def select_tile(self, tile_data):
		entity_key = tile_data.entity_key #TODO: go to update data if necessary
		self.update_data(entity_key, tile_data)

	def update_data(self, entity_key, entity_data):
		if entity_key in ENTITY_DATA_MAP:
			update_method = ENTITY_DATA_MAP[entity_key]
			update_method(self, entity_data)
		else:
			self.update_empty()

	def update_empty(self):
		current_selection_label = Label("Current selection: None")
		data_label = Label("No additional data.")
		data_label.top = current_selection_label.bottom + 8
		self.set_children([current_selection_label, data_label])

	def update_sign(self, sign_data):
		
		#TODO: add buttons which allow scrolling through different panes of sign text.
		#TODO: allow saving sign text so that it corresponds to sign_data (a specific TileData object)
			# - not sure if this alone will make it possible to give different signs different text or not
		#TODO: modify TileData reading so that a sign can be created in the leveleditor, have its text panes set, and then
			#  added to the game with the same text panes.

		sign_label = Label("Sign Text:")

		sign_text_1 = "This is a sign."
		sign_text_2 = "Press X to advance the dialog box."
		sign_text_3 = "This is the only thing any sign can ever say." #TODO: load the text from the sign's TileData.

		sign_text_lines = [sign_text_1, sign_text_2, sign_text_3]

		sign_text_entries = []
		y_offset = 16
		for s in sign_text_lines:
			next_entry = Entry(s)
			next_entry.set_minimum_size(self.width, 12)
			next_entry.padding = 4
			next_entry.top += y_offset
			y_offset += 32
			sign_text_entries.append(next_entry)

		self.set_children([sign_label])
		for s in sign_text_entries:
			self.add_child(s)
		#print sign_data #TODO
		#self.current_contents = ? #TODO

DEFAULT_SIGN = "default_sign"
ENTITY_DATA_MAP = {
		DEFAULT_SIGN:EntityDataPane.update_sign #TODO
}