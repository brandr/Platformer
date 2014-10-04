""" A special pane used in the LevelEditor fuor some (but not all) entity types to specify additional data.
"""

from ocempgui.widgets import Bin, Box, FileList, ScrolledList, Label, ImageLabel, Label, Entry, Button, ImageButton
from ocempgui.widgets.BaseWidget import *
from ocempgui.widgets import Constants #.Constants import *
from ocempgui.widgets.components import *

from pygame import Surface, Color
from pygame.draw import polygon

from cutscenescripts import MASTER_CUTSCENE_MAP

WHITE = Color("#FFFFFF")
BLACK = Color("#000000")
RED = Color("#FF0000")
GREY = Color("#999999")

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

	# SIGN
	def update_sign(self):
		sign_data = self.current_selection
		#TODO: add buttons which allow scrolling through different panes of sign text.
			# -also allow adding panes (in a different, distinct way)

		sign_label = Label("Sign Text:")
		self.sign_text_panes = sign_data.text_panes
		sign_text_entries = []

		# for i in range(0, 1): #TEMP: want to iterate through all panes eventually
		sign_text_lines = self.sign_text_panes[0]
		y_offset = 16
		for s in sign_text_lines:
			next_entry = Entry(s)
			next_entry.set_minimum_size(self.width, 12)
			next_entry.padding = 4
			next_entry.top += y_offset
			y_offset += 24
			sign_text_entries.append(next_entry)

		self.set_children([sign_label])	
		self.sign_entry_set = sign_text_entries
		for s in self.sign_entry_set:
			self.add_child(s)

		bottom_entry = self.sign_entry_set[-1]
		save_sign_button = self.save_sign_button(bottom_entry.left, bottom_entry.bottom + 8)
		self.prev_pane_button = self.build_prev_pane_button(save_sign_button.right + 8, save_sign_button.top + 4, False)
		self.next_pane_button = self.build_next_pane_button(self.prev_pane_button.right + 8, self.prev_pane_button.top, len(self.sign_text_panes) > 1)
		add_sign_pane_button = self.add_sign_pane_button(self.next_pane_button. right + 8, self.next_pane_button.top)
		self.add_child(save_sign_button)
		self.add_child(self.prev_pane_button)
		self.add_child(self.next_pane_button)
		self.add_child(add_sign_pane_button)
		self.pane_index = 0

	def change_current_sign_pane(self, pane_index):
		sign_text_lines = self.sign_text_panes[pane_index]
		y_offset = 16
		for i in range(len(sign_text_lines)):
			self.sign_entry_set[i].text = sign_text_lines[i]

	def save_sign_button(self, x, y):
		button = Button("Save current pane")
		button.topleft = x, y
		button.connect_signal(SIG_CLICKED, self.save_sign_data)	
		return button

	def save_sign_data(self):
		i = self.pane_index
		for j in range(0, 4):
			next_entry = self.sign_entry_set[j]
			next_text = next_entry.text	
			self.sign_text_panes[i][j] = next_text
		self.current_selection.set_sign_text(self.sign_text_panes)

	def add_sign_pane_button(self, x, y):
		button = Button("Add pane")
		button.topleft = x, y
		button.connect_signal(SIG_CLICKED, self.add_sign_pane)	
		return button

	def add_sign_pane(self):
		next_pane_lines = ["", "", "", ""]
		self.sign_text_panes.append(next_pane_lines)
		self.set_sensitivity(self.next_pane_button, True)

	# CUTSCENE TRIGGER
	def update_cutscene_trigger(self):
		self.current_cutscene_key = None
		cutscene_trigger_data = self.current_selection
		self.cutscene_label = Label("Linked cutscene: None") #TODO: actually figure out which cutscene is stored (use cutscene_trigger_data)
		cutscene_key = cutscene_trigger_data.cutscene_key
		if cutscene_key: self.cutscene_label.set_text("Linked cutscene: " + cutscene_key)
		self.set_children([self.cutscene_label])
		self.cutscene_select_list = self.cutscene_trigger_select_list(self.cutscene_label.rect.left, self.cutscene_label.rect.bottom + 8, 360, 200) #TEMP dimensions
		self.add_child(self.cutscene_select_list)

	def cutscene_trigger_select_list(self, x, y, width, height):
		trigger_select_list = ScrolledList(width, height)
		for cutscene_key in MASTER_CUTSCENE_MAP:
			trigger_select_list.items.append(TextListItem(cutscene_key))
		trigger_select_list.topleft = x, y
		trigger_select_list.connect_signal(SIG_SELECTCHANGED, self.change_cutscene_selection, trigger_select_list)
		return trigger_select_list

	def change_cutscene_selection(self, trigger_select_list):
		text_list_item = trigger_select_list.get_selected()[0]
		if not text_list_item: return
		self.current_cutscene_key = text_list_item._text
		self.cutscene_label.set_text("Linked cutscene: " + self.current_cutscene_key)
		self.current_selection.cutscene_key = self.current_cutscene_key

	# GENERAL METHODS
	def set_sensitivity(self, component, sensitive):
		state = Constants.STATE_INSENSITIVE
		if(sensitive): state = Constants.STATE_NORMAL
		component.set_state(state)
		component.sensitive = sensitive

	def build_prev_pane_button(self, x, y, has_prev):
		prev_image = None
		prev_image = EntityDataPane.draw_prev_image(BLACK)
		prev_button = ImageButton(prev_image)
		prev_button.topleft = x, y
		prev_button.connect_signal(SIG_CLICKED, self.sign_pane_back)
		self.set_sensitivity(prev_button, has_prev)
		return prev_button

	@staticmethod
	def draw_prev_image(color):
		prev_image = Surface((24, 24))
		prev_image.fill(WHITE)
		polygon(prev_image, color, [(24, 0), (0, 12), (24, 24)])
		return prev_image

	def build_next_pane_button(self, x, y, has_next):
		next_image = None
		next_image = EntityDataPane.draw_next_image(BLACK)
		next_button = ImageButton(next_image)
		next_button.topleft = x, y
		next_button.connect_signal(SIG_CLICKED, self.sign_pane_next)
		self.set_sensitivity(next_button, has_next)
		return next_button

	@staticmethod
	def draw_next_image(color):
		next_image = Surface((24, 24))
		next_image.fill(WHITE)
		polygon(next_image, color, [(0, 0), (0, 24), (24, 12)])
		return next_image

	def sign_pane_back(self):
		self.pane_index -= 1
		self.change_current_sign_pane(self.pane_index)
		self.update_pane_buttons()

	def sign_pane_next(self):
		self.pane_index += 1
		self.change_current_sign_pane(self.pane_index)
		self.update_pane_buttons()

	def update_pane_buttons(self):
		has_prev = self.pane_index > 0
		self.set_sensitivity(self.prev_pane_button, has_prev)
		has_next = self.pane_index < len(self.sign_text_panes) - 1
		self.set_sensitivity(self.next_pane_button, has_next)

DEFAULT_SIGN = "default_sign"
DEFAULT_CUTSCENE_TRIGGER = "default_cutscene_trigger"
ENTITY_DATA_MAP = {
		DEFAULT_SIGN:EntityDataPane.update_sign,
		DEFAULT_CUTSCENE_TRIGGER:EntityDataPane.update_cutscene_trigger
}