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
		self.rect_corner = None #a corner used to draw rectangular levels
		self.selected_cells = None #TODO: make it possible to select cells

	def init_cells(self,rows,cols):
		for i in xrange (self._rows):
			for j in xrange (self._cols):
				cell = DungeonGrid.empty_cell(i,j)
				self.add_child (i, j, cell)

	def cell_at(self,coords):
		width = DUNGEON_CELL_WIDTH+10
		height = DUNGEON_CELL_HEIGHT+10
		row = int(coords[1]/height)
		col = int(coords[0]/width)
		if (row, col) not in self.grid:
			return
		cell = self.grid[(row,col)]
		return cell

	def leftClickDungeonCell(self,cell): #TODO: consider processing the click here instead
		if(cell == None): return
		if(self.rect_corner != None):
			self.draw_level_rect(cell)
			return
		self.deselect_all_cells()
		self.set_rect_corner(cell)

	def set_rect_corner(self,cell):
		self.rect_corner = cell
		cell.select()

	#draw a rectangle using the current rect_corner and cell arg as opposite corners
	def draw_level_rect(self,corner2):
		if(corner2 == self.rect_corner):
			self.rect_corner = None
			return
		corner1 = self. rect_corner
		x1,x2 = min(corner1.col,corner2.col), max(corner1.col,corner2.col)
		y1,y2 = min(corner1.row,corner2.row), max(corner1.row,corner2.row)
		for y in range (y1,y2+1):
			for x in range(x1,x2+1):
				next_cell = self.grid[(y,x)]
				if next_cell.cell_state != SELECTED:
					next_cell.select()
		self.rect_corner = None

	def deselect_all_cells(self):
		for y in range (self._rows):
			for x in range(self._cols):
				next_cell = self.grid[(y,x)]
				if next_cell.cell_state == SELECTED:
					next_cell.deselect()

	@staticmethod
	def empty_cell(row,col):
		return DungeonGridCell(row,col)