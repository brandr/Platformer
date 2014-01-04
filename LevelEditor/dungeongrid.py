import dungeongridcell
from dungeongridcell import *
#from ocempgui.events import EventManager

class DungeonGrid(Table): #table might not be the best source.
	def __init__(self,level_select_container,rows,cols): #is this the right order for rows and cols? not source
		Table.__init__(self,rows,cols)
		self.level_select_container = level_select_container
		self.spacing = 0
		self.padding = 0
		self.init_cells(rows,cols)
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

	def leftClickDungeonCell(self,cell):
		if(cell == None or cell.cell_state == DESELECTED): return
		if(self.rect_corner != None):
			self.draw_level_rect(cell)
			self.levelSelectUpdate()
			return
		self.deselect_all_cells(True)
		self.set_rect_corner(cell)
		self.levelSelectUpdate()

	def set_rect_corner(self,cell):
		self.rect_corner = cell
		cell.select()
		self.selected_cells = []
		while len(self.selected_cells) <= cell.row:
				self.selected_cells.append([])
		for y in range (0,cell.row+1):
			while len(self.selected_cells[y]) <= cell.col:
					self.selected_cells[y].append(None)
		self.selected_cells[cell.row][cell.col] = cell

	#draw a rectangle using the current rect_corner and cell arg as opposite corners
	def draw_level_rect(self,corner2):
		if(corner2 == self.rect_corner):
			self.rect_corner = None
			return
		self.selected_cells = []
		corner1 = self. rect_corner
		x1,x2 = min(corner1.col,corner2.col), max(corner1.col,corner2.col)
		y1,y2 = min(corner1.row,corner2.row), max(corner1.row,corner2.row)
		if not self.valid_level_rect(x1,y1,x2,y2):
			self.rect_corner = None
			return
		while len(self.selected_cells) <= y2:
				self.selected_cells.append([])
		for y in range (0,y2+1):
			while len(self.selected_cells[y]) <= x2:
					self.selected_cells[y].append(None)

		for y in range (y1,y2+1):
			for x in range(x1,x2+1):
				next_cell = self.grid[(y,x)]
				self.selected_cells[y][x] = next_cell
				if next_cell.cell_state != SELECTED:
					next_cell.select()
		self.rect_corner = None

	def valid_level_rect(self,x1,y1,x2,y2):
		for y in range (y1,y2+1):
			for x in range(x1,x2+1):
				next_cell = self.grid[(y,x)]
				if next_cell.cell_state == DESELECTED: return False
		return True

	def deselect_all_cells(self,set_empty = False):
		self.selected_cells = None
		for y in range (self._rows):
			for x in range(self._cols):
				next_cell = self.grid[(y,x)]
				if next_cell.cell_state == SELECTED:
					next_cell.deselect(set_empty)

	def levelSelectUpdate(self):
		level_cell = self.level_select_container.selected_level_cell
		if level_cell == None: return
		level_cell.set_rooms(self.selected_cells)

	#def setSelectedLevelCell(self,level_cell):
	def resetRooms(self): #reset currently selected rooms to match currently selected level cell.
		level_cell = self.level_select_container.selected_level_cell
		self.rect_corner = None
		self.deselect_all_cells(False)#not sure about this True yet
		if(level_cell == None): return
		selected_cells = level_cell.room_cells
		self.selected_cells = selected_cells
		if(selected_cells == None):return
		rows = len(selected_cells)
		cols = len(selected_cells[0])
		for y in range (0, rows):
			for x in range (0,cols):
				next_room = selected_cells[y][x]
				if(next_room != None):
					self.grid[(y,x)].select()
		#TODO: if selected_cells is not None, fill


	@staticmethod
	def empty_cell(row,col):
		return DungeonGridCell(row,col)