from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from pygame import *
from leveleditorcontainer import *
from leveldata import * #might not be necessary if this is reachable through other imports

CELL_WIDTH = 242
CELL_HEIGHT = 36 
#not yet sure if the cell should store level data, or simply be used to create it. (I would prefer the latter.)
class LevelSelectCell(Table):
	def __init__(self, name, sunlit = False):	#might want to build the cell from a levelData object
		Table.__init__(self, 1, 1) 
		self.set_minimum_size(CELL_WIDTH, CELL_HEIGHT)
		self.name = name#TODO:consider retrieving from self.level_data instead
		self.name_label = Label(self.name)
		self.add_child(0, 0, self.name_label)
		self.room_cells = None
		self.sunlit = sunlit
		
	def get_name(self): #TODO: consider making this getter access level data instead.
		return self.name

	def get_level_data(self): #add other information here if more is needed for level data.
		if (self.room_cells == None): return LevelData(self.name, None, None, self.sunlit)
		origin = self.origin()
		lower_right = self.lower_right()
		data = LevelData(self.name, origin, lower_right, self.sunlit)
		return data

	def origin(self): #find the upper left corner of the level
		if self.room_cells == None: return None #might not be right. also, deal with empty levels.
		total_height = len(self.room_cells)
		total_width = len(self.room_cells[0])
		for y in range (0,total_height):
			for x in range(0, total_width):
				if self.room_cells[y][x] != None:
					return x, y
		return 0, 0 #might not be the best default

	def lower_right(self):
		total_height = len(self.room_cells)
		total_width = len(self.room_cells[0])
		return total_width - 1, total_height - 1

	def aligned_rooms(self):
		total_height = len(self.room_cells)
		total_width = len(self.room_cells[0])
		rooms = []
		origin = self.origin()
		aligned_y = 0
		for y in range(origin[1], total_height):
			rooms.append([])
			for x in range(origin[0], total_width):
				rooms[aligned_y].append(self.room_cells[y][x])
			aligned_y += 1
		return rooms

		#takes a set of dungeongridcells and connects them to this level cell.
	def set_rooms(self, dungeon_cells):
		self.room_cells = dungeon_cells #not sure this is what we want, but using it for now

	def add_entity(self, tile_data, col, row):
		room_offset = self.origin()
		room_col = col/ROOM_WIDTH	#make sure we have access to these
		room_row = row/ROOM_HEIGHT
		adjusted_room_col = room_col + room_offset[0]
		adjusted_room_row = room_row + room_offset[1]
		relative_col = col%ROOM_WIDTH
		relative_row = row%ROOM_HEIGHT
		self.room_cells[adjusted_room_row][adjusted_room_col].add_entity(tile_data, relative_col, relative_row)

	#could probabaly shorten tile_at and add_entity with an accessory method
	def tile_at(self, col, row):
		room_offset = self.origin()
		room_col = col/ROOM_WIDTH	#make sure we have access to these
		room_row = row/ROOM_HEIGHT
		adjusted_room_col = room_col + room_offset[0]
		adjusted_room_row = room_row + room_offset[1]
		relative_col = col%ROOM_WIDTH
		relative_row = row%ROOM_HEIGHT
		return self.room_cells[adjusted_room_row][adjusted_room_col].tile_at(relative_col, relative_row)

	def updateSunlit(self, sunlit):
		self.sunlit = sunlit
	
	def rename_level(self, level_name):
		self.name = level_name
		self.name_label.set_text(level_name)

	def select(self):
		self.set_state(Constants.STATE_ACTIVE)

	def deselect(self):
		self.set_state(Constants.STATE_NORMAL)