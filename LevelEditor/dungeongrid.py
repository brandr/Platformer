import dungeongridcell
from dungeongridcell import *
from ocempgui.events import EventManager

class DungeonGrid(Table): #table might not be the best source.
	def __init__(self,rows,cols): #is this the right order for rows and cols? not source
		Table.__init__(self,rows,cols)
		self.spacing = 0
		self.padding = 0
		self.init_cells(rows,cols)
		self.manager = EventManager()

	def init_cells(self,rows,cols):
		for i in xrange (self._rows):
			for j in xrange (self._cols):
				cell = DungeonGrid.empty_cell()
				self.add_child (i, j, cell)

	def cell_at(self,coords):
		width = DUNGEON_CELL_WIDTH
		height = DUNGEON_CELL_HEIGHT
		row = int(coords[1]/height)
		col = int(coords[0]/width)
		if (row, col) not in self.grid:
			return
		cell = self.grid[(row,col)]
		return cell

	def clickDungeonCell(self,cell):
		if(cell == None): return
		cell.test_click()
		
	@staticmethod
	def empty_cell():
		return DungeonGridCell()