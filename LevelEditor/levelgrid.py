from leveltilecell import *
from roomdata import *
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

LEFT_MOUSE_BUTTON = 1      #NOTE: this variable is repeated in dungeongridcontainer.py. Not sure if this could become a problem.
RIGHT_MOUSE_BUTTON = 3
# IDEA: middle mouse button to "paint" tiles.

TILE_WIDTH, TILE_HEIGHT = 32,32
WHITE = Color(("#FFFFFF"))
BLACK = Color(("#000000"))

#TODO: give this class the same fuctionality as before using the ImageLabel setup instead of table

class LevelGrid(ImageLabel):
	def __init__(self, level_editor):
		self.level_editor = level_editor
		level_cell = self.level_cell()
		room_cols, room_rows = self.get_room_dimensions()
		self.cols, self.rows = room_cols*ROOM_WIDTH,room_rows*ROOM_HEIGHT
		self.grid_image = LevelGrid.empty_grid_image(self.cols,self.rows)
		self.drawGridlines()
		ImageLabel.__init__(self,self.grid_image)
		room_cells = level_cell.aligned_rooms()
		self.init_cells(room_cells,room_rows,room_cols)

	def drawGridlines(self):
		pixel_width, pixel_height = self.get_pixel_width(), self.get_pixel_height()
		for x in range(0, self.cols):
			pygame.draw.line(self.grid_image, BLACK, (x*TILE_WIDTH, 0), (x*TILE_HEIGHT, pixel_height))
		for y in range (0, self.rows):
			pygame.draw.line(self.grid_image, BLACK, (0, y*TILE_HEIGHT), (pixel_width, y*TILE_HEIGHT))

	def get_pixel_width(self):
		return self.cols*TILE_WIDTH

	def get_pixel_height(self):
		return self.rows*TILE_HEIGHT
		
	def init_cells(self, room_cells, rows, cols):
		for i in xrange (rows):
			rooms = self.level_cell().aligned_rooms()
			for j in xrange (cols):
				cell = room_cells[i][j]
				self.add_room(i, j, cell)

	def add_room(self, row, col, room_cell):
		if room_cell.room_data == None:
			room_cell.init_room_data(ROOM_WIDTH, ROOM_HEIGHT)
			return
		room_data = room_cell.room_data
		origin_x, origin_y = col*ROOM_WIDTH,row*ROOM_HEIGHT
		for y in range (origin_y, origin_y + ROOM_HEIGHT):
			for x in range(origin_x, origin_x + ROOM_WIDTH):
				tile_data = room_data.tile_at(x - origin_x, y - origin_y)
				self.add_tile_cell(tile_data, x, y)

	def add_tile_cell(self, tile_data, x, y):
		if(tile_data == None or isinstance(tile_data, BlockedTileData)): return
		self.updateTileImage(tile_data.get_image(), x, y)

	def updateTileImage(self,image,x,y):
		tile_image = image
		pygame.draw.line(tile_image, BLACK, (0, 0), (0, TILE_HEIGHT))
		pygame.draw.line(tile_image, BLACK, (0, 0), (TILE_WIDTH, 0))
		self.grid_image.blit(tile_image, (x*TILE_WIDTH, y*TILE_HEIGHT))
		self.set_picture(self.grid_image)

	def level_cell(self):
		return self.level_editor.level_cell

	def get_room_dimensions(self):
		level_cell = self.level_cell()
		room_cells = level_cell.room_cells
		x1, y1 = level_cell.origin()
		width, height = 0, 0
		for y in range(y1, len(room_cells)):
			height += 1
		for x in range(x1, len(room_cells[0])):
			width += 1
		return width, height

	def create_cell(self, tile_data):
		cell = LevelTileCell(tile_data)
		return cell

	def valid_coords(self, coords):
		return coords[0] >= 0 and coords[0] < self.cols and coords[1] >= 0 and coords[1] < self.rows

	def processClick(self, event, calculate_offset): #TODO: somewhere in here, load additional data if necessary.
		offset = calculate_offset()
		pos = event.pos 
		adjusted_pos = ((pos[0] - offset[0] - 3,pos[1] - offset[1] + 15))#this bit is still a little wonky, but functional for now.
		coordinate_x = int(adjusted_pos[0]/(TILE_WIDTH))
		coordinate_y = int(adjusted_pos[1]/(TILE_HEIGHT))
		coordinate_pos = (coordinate_x, coordinate_y) 
		if not self.valid_coords(coordinate_pos):return
		if event.button == LEFT_MOUSE_BUTTON:
			self.leftClick(coordinate_pos[1], coordinate_pos[0])
		elif event.button == RIGHT_MOUSE_BUTTON:
			self.rightClick(coordinate_pos[1], coordinate_pos[0])
		else:
			self.leftClick(coordinate_pos[1], coordinate_pos[0]) #TEMP
			#print event
			#TODO: other click types (maybe middle mouse?)
			return

	def leftClick(self, row, col):
		tile = self.level_editor.entity_select_container.current_entity 
		if (tile == None or not self.room_for_tile(tile, row, col)): 
			self.select_cell(row, col)
			return
		existing_tile = self.tile_at(row, col)
		if existing_tile != None: 
			self.select_cell(row, col)
			return
		self.addEntity(tile, row, col)

	def select_cell(self, row, col):
		tile = self.tile_at(row, col)
		if tile == None: return
		# TODO: allow for larger than tile size 1
		# TODO: make selection visually clear. (maybe a red outline)
		# TODO: make sure different objects can have data set differently this way.
		# maybe make a "save data" button in EntityDataPane?
		# TODO: implement and test for a one-pane sign before expanding to anything else
		self.level_editor.select_tile(tile)

	def addEntity(self, tile, row, col):
		width, height = tile.width, tile.height
		self.level_cell().add_entity(tile, col, row) 	#this will be important to setting data differently for different signs
		for x in range(col + 1,col + width):
			next_block = BlockedTileData(tile, col, row)
			self.level_cell().add_entity(next_block, x, row)
		for y in range(row + 1, row + height):
			for x in range(col, col + width):
				next_block = BlockedTileData(tile, col, row)
				self.level_cell().add_entity(next_block, x, y)
		image = tile.get_image() 		#this part only needs to be done once.
		self.updateTileImage(image, col, row)

	def rightClick(self, row, col):
		tile = self.tile_at(row, col)
		if tile == None: return
		if(isinstance(tile, BlockedTileData)):
			origin_tile = tile.origin_tile
			self.removeEntity(tile.origin_y, tile.origin_x, origin_tile.width, origin_tile.height)
			return
		self.removeEntity(row, col, tile.width, tile.height)

	def removeEntity(self, row, col, width, height):
		for y in range(row, row + height):
			for x in range(col, col + width):
				self.level_cell().add_entity(None, x, y) 
				image = LevelGrid.empty_tile_image()
				self.updateTileImage(image, x, y)

	def room_for_tile(self, tile, row, col): #make sure any tile larger that 1x1 will fit in the room.
		end_x = col + tile.width - 1
		end_y = row + tile.height - 1
		return (end_x < self.cols and end_y < self.rows)

	def tile_at(self, row, col):
		return self.level_cell().tile_at(col, row)

	@staticmethod
	def empty_grid_image(cols, rows):
		image = Surface((cols*TILE_WIDTH, rows*TILE_HEIGHT))
		image.fill(WHITE)
		return image

	@staticmethod
	def empty_tile_image():
		image = Surface((TILE_WIDTH, TILE_HEIGHT))
		image.fill(WHITE)
		return image