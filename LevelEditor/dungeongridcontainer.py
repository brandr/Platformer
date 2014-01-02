import dungeongrid
from dungeongrid import *

MAX_DUNGEON_ROWS = 16
MAX_DUNGEON_COLS = 16

class DungeonGridContainer(Box):
	def __init__(self,position,dimensions):
		Box.__init__(self,dimensions[0],dimensions[1])
		self.topleft = (position[0],position[1])

		level_select_label = Label("Dungeon Grid:")

		self.dungeon_grid = DungeonGrid(MAX_DUNGEON_ROWS,MAX_DUNGEON_COLS)
		self.dungeon_window = self.dungeon_window(dimensions[0]-36,dimensions[1]-128,self.dungeon_grid)#TODO

		self.add_child(level_select_label)
		self.add_child(self.dungeon_window)

	def dungeon_window(self,width,height,dungeon_grid):
		window = ScrolledWindow(width,height)
		window.set_child(dungeon_grid)
		#window.connect_signal(SIG_MOUSEDOWN,self.clickLevelCell) #TODO: make it possible to select grid parts
		window.topleft = (18,45)
		return window
