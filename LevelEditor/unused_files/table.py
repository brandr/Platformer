import guicomponent
from guicomponent import*

#tables are similar to grids, so we may merge them later (or set up some kind of inheritance)
#TODO: make a completely empty table possible
class Table(GuiComponent):
	def __init__(self,x,y,rows,cols,cell_dimensions,initial_cells,bg = WHITE):
		width,height = rows*cell_dimensions[0],cols*cell_dimensions[1]
		GuiComponent.__init__(self,x,y,width,height,bg)
		self.cell_width,self.cell_height = cell_dimensions[0],cell_dimensions[1]
		self.cells = []
		self.initCells(initial_cells,rows,cols)

	def initCells(self,initial_cells,rows,cols):
		for y in range(0,cols):
			self.cells.append([])
			for x in range(0,rows):
				self.cells[y].append(initial_cells[y][x])

	def update(self):
		self.image = Surface((self.width,self.height))
		self.image.fill(self.bg)
		self.update_cells()
		self.draw_gridlines()

	def update_cells(self):
		for y in range(0,self.rows()):
			for x in range(0,self.cols()):
				c = self.cells[y][x]
				if c != None:
					c.update()
					self.image.blit(c.image,(x*self.cell_width,y*self.cell_height))

	def draw_gridlines(self):
		cell_width,cell_height = self.cell_width,self.cell_height
		for y in range (0,self.rows()):
			pygame.draw.line(self.image,BLACK,(0,y*cell_height),(self.width*cell_width,y*cell_height))
		for x in range(0,self.cols()):
			pygame.draw.line(self.image,BLACK,(x*cell_width,0),(x*cell_width,self.height*cell_height))

	def insertRow(self,arg):#TODO: figure out what "arg" will be (probably data for the inserted row)
		self.cells.append([])
		index = len(self.cells) - 1  #consider taking index as an arg instead
		for x in range(0,self.rows()):
			self.cells[index].append(None)
		self.height += self.cell_height

	def rows(self):
		if(len(self.cells) < 1): return 0
		return len(self.cells)

	def cols(self):
		return len(self.cells[0])