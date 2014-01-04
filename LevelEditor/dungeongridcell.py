from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from pygame import *

DUNGEON_CELL_WIDTH = 24
DUNGEON_CELL_HEIGHT = 24

SELECTED = "selected"
EMPTY = "empty"

class DungeonGridCell(ImageButton):

	def __init__(self,row,col): #TODO: consider making it possible to init non-empty cells
		ImageButton.__init__(self,"")
		self.minsize = DUNGEON_CELL_WIDTH,DUNGEON_CELL_HEIGHT
		#self.connect_signal(SIG_CLICKED,self.test_click)
		self.set_picture(DungeonGridCell.empty_level_tile())
		self.cell_state = EMPTY
		self.row,self.col = row,col

	def select(self):
		self.set_picture(DungeonGridCell.selected_level_tile())
		self.cell_state = SELECTED

	def deselect(self): #TODO: should only be empty when the room is not part of a level
		self.set_picture(DungeonGridCell.empty_level_tile())
		self.cell_state = EMPTY

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
