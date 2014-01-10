from tiledata import *

ROOM_WIDTH = 10
ROOM_HEIGHT = 8

class RoomData(object):
	"""docstring for RoomData"""
	def __init__(self,width,height,x,y):
		self.global_x,self.global_y = x,y
		self.tiles = RoomData.empty_tile_set(width,height)
	
	def empty(self):
		for row in self.tiles:
			for t in row:
				if t != None: return False #NOTE: because of this, if we make it possible to clear tiles, doing so should set those tiles to None.
		return True

	def tile_at(self,x,y):
		return self.tiles[y][x]

	def setAllTiles(self,tile_set):
		rows, cols = len(tile_set),len(tile_set[0])
		for y in xrange(rows):
			for x in xrange(cols):
				self.tiles[y][x] = tile_set[y][x]
	
	def set_tile(self,tile_data,col,row):
		self.tiles[row][col] = tile_data #might benefit from a special setter if tiledata becomes more complex.

	def formatted_data(self):
		return (self.global_x,self.global_y,self.formatted_tile_set()) #might need to format tiles

	def formatted_tile_set(self):
		tiles = []
		for y in xrange (len(self.tiles)):
			tiles.append([])
			for x in xrange(len(self.tiles[y])):
				next_data = None
				next_tile = self.tiles[y][x]
				if next_tile != None:
					next_data = next_tile.formatted_data()
				tiles[y].append(next_data)
		return tiles

	@staticmethod
	def deformatted_room_set(formatted_data):
		rooms = []
		for y in xrange (len(formatted_data)):
			rooms.append([])
			for x in xrange(len(formatted_data[y])):
				next_data = None
				next_room = formatted_data[y][x]
				if next_room != None:
					next_data = RoomData.deformatted_room(next_room)
				rooms[y].append(next_data)
		return rooms

	@staticmethod
	def deformatted_room(formatted_data):
		x,y = formatted_data[0],formatted_data[1]
		tile_set = TileData.deformatted_tile_set(formatted_data[2]) #have to deformat tiles before returning the room_data.
		width,height = len(tile_set[0]),len(tile_set) #might need a None exeception handler
		room_data = RoomData(width,height,x,y)
		room_data.setAllTiles(tile_set)
		return room_data

	@staticmethod
	def empty_tile_set(width,height):
		tiles = []
		for y in xrange(height):
			tiles.append([])
			for x in xrange(width):
				tiles[y].append(None)
		return tiles