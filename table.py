import guicomponent
from guicomponent import*

#tables are similar to grids, so we may merge them later (or set up some kind of inheritance)
#TODO: make a completely empty table possible
class Table(GuiComponent):
	def __init__(self,x,y,rows,cols,cell_dimensions,bg = WHITE):
		width,height = rows*cell_dimensions[0],cols*cell_dimensions[1]
		GuiComponent.__init__(self,x,y,width,height,bg)
		self.rows,self.cols = rows,cols
		self.cell_width,self.cell_height = cell_dimensions[0],cell_dimensions[1] 

	def update(self):
		self.draw_gridlines()

	def draw_gridlines(self):
		cell_width,cell_height = self.cell_width,self.cell_height
		for y in range (0,self.cols):
			pygame.draw.line(self.image,BLACK,(0,y*cell_height),(self.width*cell_width,y*cell_height))
		for x in range(0,self.rows):
			pygame.draw.line(self.image,BLACK,(x*cell_width,0),(x*cell_width,self.height*cell_height))