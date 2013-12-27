#a grid is a rectangular array of buttons. (may make it less specific if we need grids for anything else.)
import button
from button import *

class Grid(object):
	#TODO: consider making grid inherit from guicomponent.

	def __init__(self,x,y,width,height,tile_size): #TODO: consider including button type here, along with maybe button data (both with defaults, probably)
		self.x,self.y = x,y
		self.image = Surface((width*tile_size+1,height*tile_size+1)) #+1s needed to fit gridlines
		self.image.fill(BLACK)
		self.tile_size = tile_size
		self.buttons = []
		if(width <= 0 or height <= 0):return
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
		self.draw_gridlines()

	def draw_gridlines(self):
		tile_size = self.tile_size
		for y in range (0,self.height()):
			pygame.draw.line(self.image,BLACK,(0,y*tile_size),(self.width()*tile_size,y*tile_size))
		for x in range(0,self.width()):
			pygame.draw.line(self.image,BLACK,(x*tile_size,0),(x*tile_size,self.height()*tile_size))

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

	@staticmethod
	def blank_grid_tile(tile_size):
		blank_tile = Surface((tile_size,tile_size))
		blank_tile.fill(WHITE)
		return blank_tile

	@staticmethod
	def grid_box(tile_size):
		transparent = Surface(tile_size-2,tile_size-2)
		transparent
		box = Surface(tile_size,tile_size)
		return box

	#trims a tile to fit within gridlines, then returns it
	@staticmethod	
	def grid_tile(full_tile):
		grid_tile = Surface((full_tile.get_width()-2,full_tile.get_height()-2))
		grid_tile.blit(full_tile, (1, 1), (1, 1, grid_tile.get_width(), grid_tile.get_height()))
		return grid_tile