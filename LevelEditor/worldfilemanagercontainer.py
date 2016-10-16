from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
import os

class WorldFileManagerContainer(Box):
	def __init__(self, dungeon_select_container, position, dimensions):
		#init basic attributes
		Box.__init__(self, dimensions[0], dimensions[1])
		self.topleft = (position[0], position[1])
		self.dungeon_select_container = dungeon_select_container

		#create components
		self.new_world_button = self.new_world_button(8, dimensions[1] - 84)
		self.save_world_button = self.save_world_button(self.new_world_button.right + 8, self.new_world_button.top)
		self.load_world_button = self.load_world_button(self.save_world_button.right + 8, self.save_world_button.top)
		self.current_file_label = self.current_file_label(8, 8)
		self.filename_entry = self.filename_entry(self.current_file_label.right + 8, self.current_file_label.top - 4)
		self.file_select_window = self.file_select_window(self.current_file_label.left, self.current_file_label.bottom + 8)

		self.add_child(self.new_world_button)
		self.add_child(self.save_world_button)
		self.add_child(self.load_world_button)
		self.add_child(self.file_select_window)
		self.add_child(self.filename_entry)
		self.add_child(self.current_file_label)
		self.updateFileSelection()
		self.setSensitivity(self.save_world_button, True) #TEMP

	def new_world_button(self, x, y):
		button = Button("New World")
		button.topleft = x, y
		#TODO: create a new world with the given name if possible. May need to reset the editor.
		#button.connect_signal(SIG_CLICKED, self.level_select_container.editor_screen.resetEditor) 
		return button

	def save_world_button(self, x, y):
		button = Button("Save World")
		button.topleft = x, y
		button.connect_signal(SIG_CLICKED, self.saveWorld)
		return button

	def load_world_button(self, x, y):
		button = Button("Load World")
		button.topleft = x, y
		button.connect_signal(SIG_CLICKED, self.loadWorld)
		return button

	def current_file_label(self, x, y):
		label = Label ("Selected save: ")
		label.topleft = x, y
		return label

	def filename_entry(self, x, y):
		entry = Entry("                  ") # all these spaces are only to set the size
		entry.set_text("")
		entry.topleft = x, y
		return entry

	def file_select_window(self, x, y): 
		file_list = FileList (224, 200, "./world_files")
		file_list.topleft = x, y
		file_list.connect_signal(SIG_SELECTCHANGED, self.change_selection, file_list)
		return file_list

	def setSensitivity(self, component, sensitive):
		state = Constants.STATE_INSENSITIVE
		if(sensitive): state = Constants.STATE_NORMAL
		component.set_state(state)
		component.sensitive = sensitive

	def saveWorld(self):
		pass #TODO

	def loadWorld(self):
		pass #TODO

	#methods for file slot selection

	def current_filename(self):
		return self.filename_entry._text

	def change_selection(self, window):
		selected_file = self.file_select_window.get_selected()
		filename = selected_file[0]._text
		self.filename_entry.set_text(filename)	# error checking?
		self.updateFileSelection()
	
	def updateFileSelection(self):
		current_filename = self.current_filename()
		valid_filename = current_filename != None and len(current_filename) > 0	and current_filename != ".." #TODO: consider checking for spaces and stuff too
		#self.setSensitivity(self.save_world_button, valid_filename)
		self.setSensitivity(self.load_world_button, valid_filename)