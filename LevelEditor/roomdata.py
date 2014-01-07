from tiledata import *

class RoomData(object):
	"""docstring for RoomData"""
	def __init__(self,width,height):#, arg): #TODO
		self.tiles = RoomData.empty_tile_set(width,height)
		
	def tile_at(self,x,y):
		return self.tiles[y][x]
	
	def set_tile(self,tile_data,col,row):
		self.tiles[row][col] = tile_data #might benefit from a special setter if tiledata becomes more complex.

	@staticmethod
	def empty_tile_set(width,height):
		tiles = []
		for y in xrange(height):
			tiles.append([])
			for x in xrange(width):
				tiles[y].append(None)
		return tiles