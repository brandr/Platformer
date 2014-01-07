#NOTE: this class might need to be accessed by classes outside the leveleditor.

#TODO: store tiles in rooms instead, and associate LevelData with those rooms.
class LevelData(object):
	"""docstring for LevelData"""
	def __init__(self,rows,cols):
		self.tiles = LevelData.empty_tile_set(rows,cols)

	def images(self):
		images = []
		for y in xrange(len(self.tiles)):
			images.append([])
			for x in xrange(len(self.tiles[y])):
				images[y].append(self.tiles[y][x]) #TODO: make this part a data member of self.tiles once tiles are more complex.
		return images

	def add_entity(self,image,col,row): #TODO: change "image" eventually.
		self.tiles[row][col] = image

	@staticmethod
	def empty_tile_set(rows,cols):
		tiles = []
		for y in xrange(rows):
			tiles.append([])
			for x in xrange(cols):
				tiles[y].append(None)
		return tiles