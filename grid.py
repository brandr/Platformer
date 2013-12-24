#a grid is a rectangular array of buttons. (may make it less specific if we need grids for anything else.)
import button
from button import *

class Grid(object):
	#TODO: consider making grid inherit from guicomponent.

	def __init__(self,x,y,width,height,tile_size): #TODO: consider including button type here, along with maybe button data (both with defaults, probably)
		self.x,self.y = x,y
		#self.width,self.height = (width,height)
		self.image = Surface((width*tile_size,height*tile_size))
		self.image.fill(BLACK)
		self.tile_size = tile_size
		self.buttons = []
		if(width <= 0 or height <= 0):return
		#self.initBackground() #not sure if I'll actually use this
		for y in range (0,height):
			self.buttons.append([])
			for x in range(0,width):
				blank_button = Grid.blank_grid_button(tile_size,x,y)
				self.buttons[y].append(blank_button)
				
	def update(self):
		for row in self.buttons:
			for b in row:
				b.update()
				self.image.blit(b.image,(b.x*self.tile_size,b.y*self.tile_size))

	def button_at(self,pos):
		if(not self.valid_button_pos(pos)): return None
		x_coord = pos[0]/self.tile_size
		y_coord = pos[1]/self.tile_size
		return self.buttons[y_coord][x_coord]

	def valid_button_pos(self,pos):
		xcheck = 0 <= pos[0] < self.tile_size*len(self.buttons[0])
		ycheck = 0 <= pos[1] < self.tile_size*len(self.buttons)

		return xcheck and ycheck

	def contains(self,pos):
		#if(not self.y <= pos[1] <=self.height()*self.tile_size):
		#	print (str((self.x,self.y))+", "+str(pos))
		return (self.x <= pos[0] <= self.x+self.width()*self.tile_size and self.y <= pos[1] <=self.y+self.height()*self.tile_size)

	def relative_pos(self,pos):
		return (pos[0]-self.x,pos[1]-self.y)

	def width(self):
		return len(self.buttons[0])

	def height(self):
		return len(self.buttons)

	@staticmethod
	def blank_grid_button(tile_size,x,y):
		button_image = Grid.blank_grid_tile(tile_size)
		return Button(button_image,x,y)

	#TODO: make an update method which blits all of the grid's buttons' images against its background.

	@staticmethod
	def blank_grid_tile(tile_size):
		blank_tile = Surface((tile_size,tile_size))
		blank_tile.fill(WHITE)
		return Grid.grid_tile(blank_tile)

	#trims a tile to fit within gridlines, then returns it
	@staticmethod	
	def grid_tile(full_tile):
		grid_tile = Surface((full_tile.get_width()-2,full_tile.get_height()-2))
		grid_tile.blit(full_tile, (1, 1), (1, 1, grid_tile.get_width(), grid_tile.get_height()))
		return grid_tile