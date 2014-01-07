from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from pygame import *

from roomdata import *

DUNGEON_CELL_WIDTH = 18
DUNGEON_CELL_HEIGHT = 18

SELECTED = "selected"
DESELECTED = "deselected"
EMPTY = "empty"

class DungeonGridCell(ImageButton):
	#a cell that reprensents a room.
	def __init__(self,row,col): #TODO: consider making it possible to init non-empty cells
		ImageButton.__init__(self,"")
		self.minsize = DUNGEON_CELL_WIDTH,DUNGEON_CELL_HEIGHT
		self.set_picture(DungeonGridCell.empty_level_tile())
		self.empty = True #TODO: if more useful, replace this with setting self.level_cell = None, or something similar
		self.cell_state = EMPTY
		self.row,self.col = row,col
		
		self.room_data = None #TODO: make it possible to alter room data after it is initialized.

	def init_room_data(self,width,height):
		self.room_data = RoomData(width,height)

	def select(self): #TODO: consider passing in level_cell arg here
		self.set_picture(DungeonGridCell.selected_level_tile())
		self.cell_state = SELECTED
		self.empty = False

	def deselect(self,set_empty = False): #TODO: should only be empty when the room is not part of a level
		self.empty = set_empty
		if self.empty:
			self.set_picture(DungeonGridCell.empty_level_tile())
			self.cell_state = EMPTY
		else:
			self.set_picture(DungeonGridCell.deselected_level_tile())
			self.cell_state = DESELECTED

	def add_entity(self,tile_data,col,row):
		self.room_data.set_tile(tile_data,col,row)

	@staticmethod
	def empty_level_tile():
		tile = Surface((DUNGEON_CELL_WIDTH,DUNGEON_CELL_HEIGHT))
		tile.fill(Color("#888888"))
		return tile

	@staticmethod
	def selected_level_tile():
		tile = Surface((DUNGEON_CELL_WIDTH,DUNGEON_CELL_HEIGHT))
		tile.fill(Color("#FF0000"))
		return tile

	@staticmethod
	def deselected_level_tile():
		tile = Surface((DUNGEON_CELL_WIDTH,DUNGEON_CELL_HEIGHT))
		tile.fill(Color("#FFAAFF"))
		return tile
