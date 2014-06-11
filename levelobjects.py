from roomdata import *

class LevelObjects(object):
	
	def __init__(self, level, tiles = None, entities = None):
		self.level = level
		self.tiles = tiles
		self.entities = entities
		self.player = None

	def get_entities(self, entity_type):
		return [e for e in self.entities if isinstance(e, entity_type)]

	def get_tiles(self):
		return self.tiles

	def addPlayer(self, player):
		self.player = player
		self.entities.append(player)

	def remove(self, entity):
		if entity in self.entities:
			self.entities.remove(entity)

	def removePlayer(self):
		self.entities.remove(self.player)
		self.player = None

	def addBlock(self,block,tile = None):
		if tile != None:
			tile.block = block
		self.addEntity(block)

	def addLevelObjects(self, room_coords, level_objects):
		if self.tiles == None:
			self.tiles = []
		if self.entities == None:
			self.entities = []
		level = self.level
		x_offset = room_coords[0] - level.origin[0]
		y_offset = room_coords[1] - level.origin[1]
		for e in level_objects.entities:
			self.entities.append(e)
			entity_x_offset = ROOM_WIDTH*x_offset
			entity_y_offset = ROOM_HEIGHT*y_offset
			if(entity_x_offset != 0 or entity_y_offset != 0):
				e.moveRect(entity_x_offset*32, entity_y_offset*32)
			e.current_level = level
		for row in level_objects.tiles:
			for t in row:
				self.addTile(t, x_offset, y_offset)

	def addEntity(self, entity):
		self.entities.append(entity)
		entity.current_level = self.level

	def addTile(self, tile, x_offset, y_offset):
		level = self.level
		new_x = tile.coordinates()[0] + ROOM_WIDTH*x_offset
		new_y = tile.coordinates()[1] + ROOM_HEIGHT*y_offset
		while len(self.tiles) <= new_y:
			self.tiles.append([])
		while len(self.tiles[new_y]) <= new_x:
			self.tiles[new_y].append(None)
		self.tiles[new_y][new_x] = tile
		tile.current_level = level
		tile.moveRect(new_x*32, new_y*32, True)