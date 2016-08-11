from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
import os

DUNGEON_NAME_SPACING = 26

class DungeonSelectContainer(Box):
	def __init__(self, position, dimensions): #TODO: add arg for connected component if necessary.
		
		Box.__init__(self, dimensions[0], dimensions[1])
		self.topleft = (position[0], position[1])
		dungeon_select_label = Label("Included Dungeons:")
		self.dungeon_window_dimensions = dimensions[0] - 64, dimensions[1] - 128
		#TODO: link dungeon selector to other components if necessary.
		self.dungeon_selector = DungeonSelector((0, 0), (dimensions[0] - 40, dimensions[1]))
		self.dungeon_window = self.create_dungeon_window(self.dungeon_window_dimensions[0], self.dungeon_window_dimensions[1], self.dungeon_selector)
		self.add_child(dungeon_select_label)
		self.add_child(self.dungeon_window)

	def create_dungeon_window(self, width, height, dungeon_selector):
		window = ScrolledWindow(width, height)
		window.set_child(dungeon_selector)
		window.topleft = (18, 45)
		window.connect_signal(SIG_MOUSEDOWN, self.clickDungeonWindow)
		return window

	def clickDungeonWindow(self, event):
		if(event.button != LEFT_MOUSE_BUTTON): return
		coords = event.pos
		screen_offset = (self.left + self.dungeon_window.left, self.top + self.dungeon_window.top)
		relative_coords = (coords[0] - screen_offset[0], coords[1] - screen_offset[1])
		if relative_coords[0] > self.dungeon_window.vscrollbar.left or relative_coords[1] > self.dungeon_window.hscrollbar.top: return
		x_scroll_offset = self.dungeon_window.hscrollbar.value
		y_scroll_offset = self.dungeon_window.vscrollbar.value
		adjusted_coords = (relative_coords[0] + x_scroll_offset, relative_coords[1] + y_scroll_offset) 
		self.dungeon_selector.handle_click(adjusted_coords)

class DungeonSelector(Box):
	def __init__(self, position, dimensions):
		Box.__init__(self, dimensions[0], dimensions[1])
		self.topleft = (position[0], position[1])
		self.init_dungeon_list()

	def init_dungeon_list(self):
		dungeon_filenames = self.load_dungeon_filenames()
		self.dungeon_checkboxes = []
		for i in xrange(len(dungeon_filenames)):
			name = dungeon_filenames[i]
			checkbox = CheckButton(name)
			checkbox.topleft = (8, i*DUNGEON_NAME_SPACING)
			self.dungeon_checkboxes.append(checkbox)
			self.add_child(checkbox)

	def load_dungeon_filenames(self):
		dungeon_filenames = []
		for f in os.listdir("./dungeon_map_files"): dungeon_filenames.append(f)
		return dungeon_filenames

	def handle_click(self, coords):
		if coords[0] < 13 or coords[0] > 25: return
		offset = coords[1] % DUNGEON_NAME_SPACING
		if offset < 8 or offset > 19: return
		index = int( (coords[1] )/DUNGEON_NAME_SPACING)
		self.dungeon_checkboxes[index].activate()