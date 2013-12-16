#all entities in a level (including player, )

class LevelObjects(object):
	def __init__(self,level,tiles,entities,platforms,lanterns):
		self.tiles = tiles
		self.entities = entities
		self.platforms = platforms
		self.lanterns = lanterns

		self.player = None

		for e in entities:
			e.current_level = level

	def addPlayer(self,player):
		self.player = player
		self.entities.add(player)

	def remove(self,entity):
		self.entities.remove(entity)
		self.platforms.remove(entity)
		self.lanterns.remove(entity)

	def removePlayer(self):
		self.entities.remove(self.player)
		self.player = None
