from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

import json

from dungeondata import *

DEFAULT_FILE_COUNT = 10

#IDEA: could indicate which slots are empty and which are not

#TODO: use Json to read/write files containing DungeonData objects.


#"Another variant of the dumps() function, called dump(), simply serializes the object to a file. So if f is a file object opened for writing, we can do this:
#json.dump(x, f)
#To decode the object again, if f is a file object which has been opened for reading:
#x = json.load(f)"

class FileManagerContainer(Box):
	"""docstring for FileManagerContainer"""
	def __init__(self, level_select_container,dungeon_grid_container,position,dimensions):
		#init basic attributes
		Box.__init__(self,dimensions[0],dimensions[1])
		self.topleft = (position[0],position[1])
		
		#init data specific to this container
		self.level_select_container, self.dungeon_grid_container = level_select_container,dungeon_grid_container
		self.selected_slot = None

		#create components
		self.new_dungeon_button = self.new_dungeon_button(8,8)
		self.save_dungeon_button = self.save_dungeon_button(self.new_dungeon_button.right+16,self.new_dungeon_button.top)
		self.load_dungeon_button = self.load_dungeon_button(self.save_dungeon_button.right+16,self.save_dungeon_button.top)
		self.selected_slot_label = self.selected_slot_label(dimensions[0]-164,8)
		self.file_slot_window = self.file_slot_window(self.selected_slot_label.left+32,self.selected_slot_label.bottom+8)
		#TODO: delete dungeon data button? Other buttons?

		#add components to contaier
		self.add_child(self.new_dungeon_button)
		self.add_child(self.save_dungeon_button)
		self.add_child(self.load_dungeon_button)
		self.add_child(self.file_slot_window)
		self.add_child(self.selected_slot_label)

		self.updateFileSelection()

	#methods for making GUI components

	def new_dungeon_button(self,x,y):
		button = Button("New Dungeon")
		button.topleft = x,y
		button.connect_signal(SIG_CLICKED,self.level_select_container.editor_screen.resetEditor) 
		return button

	def save_dungeon_button(self,x,y):
		button = Button("Save Dungeon")
		button.topleft = x,y
		button.connect_signal(SIG_CLICKED,self.saveDungeon)
		return button

	def load_dungeon_button(self,x,y):
		button = Button("Load Dungeon")
		button.topleft = x,y
		button.connect_signal(SIG_CLICKED,self.loadDungeon)
		return button

	def file_slot_window(self,x,y): 
		window = ScrolledList(72,72)
		window.topleft = x,y
		file_slot_collection = FileManagerContainer.default_file_slots()
		window.set_items(file_slot_collection)
		window.set_selectionmode(SELECTION_SINGLE)
		window.connect_signal(SIG_SELECTCHANGED,self.changeSelection,window)
		return window

	def selected_slot_label(self,x,y):
		label = Label ("Selected slot:     ")
		label.topleft = x,y
		return label

	#methods that affect components

	def setSensitivity(self,component,sensitive):
		state = Constants.STATE_INSENSITIVE
		if(sensitive): state = Constants.STATE_NORMAL
		component.set_state(state)
		component.sensitive = sensitive

	#save-related methods

	def saveDungeon(self):
		if self.selected_slot == None: return
		slot = self.selected_slot
		filename = "./dungeon_map_files/dungeon"+slot
		dungeon_file = open(filename,'wb') #'wb' means "write binary"
		dungeon_data = self.dungeon_save_data()
		save_data = dungeon_data.formatted_data()
		json.dump(save_data, dungeon_file)

	def dungeon_save_data(self): #return a DungeonData object used for reading/writing files
		#TODO: (make sure to deal with ununsed rooms/levels properly when building the DungeonData)
		level_data_set = self.level_select_container.level_save_data() 
		room_data_set = self.dungeon_grid_container.room_save_data() 
		dungeon_data = DungeonData(level_data_set,room_data_set)
		return dungeon_data

	#load method

	def loadDungeon(self):
		if self.selected_slot == None: return
		slot = self.selected_slot
		filename = "./dungeon_map_files/dungeon"+slot
		deformatted_dungeon = FileManagerContainer.dungeonDataFromFile(filename)
		self.buildDungeon(deformatted_dungeon)

	@staticmethod
	def dungeonDataFromFile(filename,filepath = "./"):
		dungeon_file = open(filename,'rb') #'rb' means "read binary"
		dungeon_data = json.load(dungeon_file) #this part reads the data from file
		deformatted_dungeon = DungeonData.deformatted_dungeon(dungeon_data,filepath)
		return deformatted_dungeon

	def buildDungeon(self,dungeon_data): #uncomment the prints in this method to test load times.
		if dungeon_data == None: return
		print "Building dungeon..."
		level_data_set = dungeon_data.level_data_set
		room_data_set = dungeon_data.rooms
		print "Resetting the editor..."
		self.level_select_container.editor_screen.resetEditor()
		#print "Loading rooms..."
		self.dungeon_grid_container.setRooms(room_data_set) #NOTE: this part is currently the most time-consuming.
		print "Loading levels..."
		self.level_select_container.setLevels(level_data_set) 
		print "Dungeon built."

	#methods for file slot selection

	def changeSelection(self,window):
		slot = self.file_slot_window.get_selected()
		self.selected_slot = None
		if slot != None and len(slot) >= 1:
			self.selected_slot = slot[0].text
		self.updateFileSelection()

	def updateFileSelection(self):
		selection_string = "Selected slot: "
		slot = self.selected_slot
		if slot == None:
			selection_string += "None"
		else:
			selection_string += str(slot)
		self.selected_slot_label.set_text(selection_string)
		self.setSensitivity(self.save_dungeon_button,self.selected_slot != None)
		self.setSensitivity(self.load_dungeon_button,self.selected_slot != None)

	#static methods

	@staticmethod
	def default_file_slots():
		slot_count = DEFAULT_FILE_COUNT
		collection = ListItemCollection()
		for n in xrange(slot_count):
			collection.append(TextListItem(str(n)))
		return collection
