from leveltilecell import *

#TODO: figure out where room dimensions should be stored.
ROOM_WIDTH = 10
ROOM_HEIGHT = 8
LEFT_MOUSE_BUTTON = 1      #NOTE: this variable is repeated in dungeongridcontainer.py. Not sure if this could become a problem.

#TODO: consider gridlines 

class LevelGrid(Table):
	def __init__(self,level_editor,rows,cols):
		self.level_editor = level_editor
		level_cell = self.level_cell()
		#room_cells = level_cell.room_cells #might make a getter for this if it helps
		cols,rows = self.get_room_dimensions()
		Table.__init__(self,rows*ROOM_HEIGHT,cols*ROOM_WIDTH)
		self.spacing = 0
		self.padding = 0
		self.init_cells(rows,cols) #might not needs args

	def get_level_data(self):
		data = [] #TODO: change the type of this as necessary. (might make leveldata its own class.)
		for y in xrange(self._rows):
			data.append([])
			for x in xrange(self._cols):
				next_data = self.grid[(y,x)].image #TODO: make this a different data member of leveltilecell instead if necessary.
				data[y].append(next_data)
		return data

	def setLevelData(self,data):
		for y in xrange(self._rows):
			for x in xrange(self._cols):
				next_image = data[y][x] #TODO: make sure this matches the data memebr in get_level_data.
				self.grid[(y,x)].set_picture(next_image)

		#IDEA: could get rows and cols from level cell insted
	def init_cells(self,rows,cols):
		for i in xrange (rows):
			rooms = self.level_cell().aligned_rooms()
			for j in xrange (cols):
				room_data = rooms[i][j]
				self.add_room(i,j,room_data)

	def add_room(self,row,col,room_data = None):
		if room_data == None:
			self.add_empty_room(row,col)
			return
		#TODO: actually use roomdata (OR decide  that resizing a level removes whatever is in it)
		#TODO: make it possible to save all room data to self.level_cell, possibly upon closing editor (could change button to "save and close")
		#there might be other ways to save, like associating each level cell with a levelgrid.

	def add_empty_room(self,row,col):
		origin_x,origin_y = col*ROOM_WIDTH,row*ROOM_HEIGHT
		for y in range (origin_y,origin_y+ROOM_HEIGHT):
			for x in range(origin_x,origin_x+ROOM_WIDTH):
				self.add_empty_tile_cell(x,y)

	def add_empty_tile_cell(self,x,y):
		cell = self.empty_cell() #Should also make a method for reading corresponding room cell at these coords.
		self.add_child (y, x, cell)

	def level_cell(self):
		return self.level_editor.level_cell

	def get_room_dimensions(self):#,room_cells):
		level_cell = self.level_cell()
		room_cells = level_cell.room_cells
		x1,y1 = level_cell.origin()
		width, height = 0,0
		for y in range(y1,len(room_cells)): #might not always be correct
			height += 1
		for x in range(x1,len(room_cells[0])):
			width += 1
		return width, height

	#@staticmethod
	def empty_cell(self):	#args might help here
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
		clicked_tile = self.grid[(coordinate_pos[0],coordinate_pos[1])]
		if event.button == LEFT_MOUSE_BUTTON:
			self.leftClick(clicked_tile)
		else:
			#TODO: other click types
			return

	def leftClick(self,clicked_tile):
		image = self.level_editor.entity_select_container.current_image()
		clicked_tile.set_picture(image)
		#TODO: need to make tiles store more useful data than just images.


		