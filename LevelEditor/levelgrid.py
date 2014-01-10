from leveltilecell import *
from roomdata import *

LEFT_MOUSE_BUTTON = 1      #NOTE: this variable is repeated in dungeongridcontainer.py. Not sure if this could become a problem.

class LevelGrid(Table):
	def __init__(self,level_editor,rows,cols):
		self.level_editor = level_editor
		level_cell = self.level_cell()
		cols,rows = self.get_room_dimensions()
		Table.__init__(self,rows*ROOM_HEIGHT,cols*ROOM_WIDTH)
		self.spacing = 0
		self.padding = 0
		room_cells = level_cell.aligned_rooms()
		self.init_cells(room_cells,rows,cols)
		
	def init_cells(self,room_cells,rows,cols):
		for i in xrange (rows):
			rooms = self.level_cell().aligned_rooms()
			for j in xrange (cols):
				cell = room_cells[i][j]
				self.add_room(i,j,cell)

	def add_room(self,row,col,room_cell):
		if room_cell.room_data == None:
			room_cell.init_room_data(ROOM_WIDTH,ROOM_HEIGHT) #might want to store these in roomdata instead, not sure.
			self.add_empty_room(row,col)
			return
		room_data = room_cell.room_data
		origin_x,origin_y = col*ROOM_WIDTH,row*ROOM_HEIGHT
		for y in range (origin_y,origin_y+ROOM_HEIGHT):
			for x in range(origin_x,origin_x+ROOM_WIDTH):
				tile_data = room_data.tile_at(x - origin_x,y - origin_y)
				self.add_tile_cell(tile_data,x,y)

	def add_empty_room(self,row,col):
		origin_x,origin_y = col*ROOM_WIDTH,row*ROOM_HEIGHT
		for y in range (origin_y,origin_y+ROOM_HEIGHT):
			for x in range(origin_x,origin_x+ROOM_WIDTH):
				self.add_empty_tile_cell(x,y)

	def add_tile_cell(self,tile_data,x,y):
		if(tile_data == None):
			self.add_empty_tile_cell(x,y)
			return
		cell = self.create_cell(tile_data)
		self.add_child (y, x, cell)

	def add_empty_tile_cell(self,x,y):
		cell = self.empty_cell() 
		self.add_child (y, x, cell)

	def level_cell(self):
		return self.level_editor.level_cell

	def get_room_dimensions(self):
		level_cell = self.level_cell()
		room_cells = level_cell.room_cells
		x1,y1 = level_cell.origin()
		width, height = 0,0
		for y in range(y1,len(room_cells)):
			height += 1
		for x in range(x1,len(room_cells[0])):
			width += 1
		return width, height

	def create_cell(self,tile_data):
		cell = LevelTileCell(tile_data)
		return cell

	def empty_cell(self):	
		cell = LevelTileCell()
		return cell

	def processClick(self,event,calculate_offset):
		offset = calculate_offset()
		pos = event.pos 
		adjusted_pos = ((pos[0]-offset[0],pos[1]-offset[1]))
		coordinate_x = int(adjusted_pos[0]/(LEVEL_TILE_WIDTH+1.1))
		coordinate_y = int(adjusted_pos[1]/(LEVEL_TILE_HEIGHT+1.25))
		coordinate_pos = (coordinate_y,coordinate_x) #this bit is still a little wonky, but functional for now.
		if(coordinate_pos not in self.grid): return
		if event.button == LEFT_MOUSE_BUTTON:
			self.leftClick(coordinate_pos[0],coordinate_pos[1])
		else:
			#TODO: other click types
			#IDEA: right click to delete
			return

	def leftClick(self,row,col):
		tile = self.level_editor.entity_select_container.current_entity 
		if tile == None: return #could also make this delete
		image = tile.get_image()
		self.level_cell().add_entity(tile,col,row)
		clicked_tile = self.grid[(row,col)]	
		clicked_tile.set_picture(image)