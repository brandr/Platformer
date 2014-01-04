from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from pygame import *

CELL_WIDTH = 242
CELL_HEIGHT = 36 

class LevelSelectCell(Table):
	def __init__(self,name):#TODO: args specific to LevelSelectCells 
		Table.__init__(self,1,1) #TODO: consider making this a label or other type
		self.set_minimum_size(CELL_WIDTH,CELL_HEIGHT)
		self.name = name#TODO:specify which level (consider retrieving frm self.level_data instead)
		self.name_label = Label(self.name)
		self.add_child(0,0,self.name_label)
		self.room_cells = None
		
	def get_name(self): #TODO: consider making this getter access level data instead.
		return self.name

		#TODO: takes a set of dungeongridcells and connects them to this level cell.
	def set_rooms(self,dungeon_cells):
		self.room_cells = dungeon_cells #not sure this is what we want, but using it for now
	
	def rename_level(self,level_name):
		self.name = level_name
		self.name_label.set_text(level_name)

	def select(self):
		self.set_state(Constants.STATE_ACTIVE)

	def deselect(self):
		self.set_state(Constants.STATE_NORMAL)