import dungeongridcell
from dungeongridcell import *

class DungeonGrid(Table): #table might not be the best source.
	def __init__(self,rows,cols): #is this the right order for rows and cols? not source
		Table.__init__(self,rows,cols)
		self.spacing = 0
		self.padding = 0
		self.init_cells(rows,cols)

	def init_cells(self,rows,cols):
		for i in xrange (self._rows):
			for j in xrange (self._cols):
				cell = DungeonGrid.empty_cell()
				self.add_child (i, j, cell)

	@staticmethod
	def empty_cell():
		return DungeonGridCell()