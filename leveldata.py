#NOTE: this class might need to be accessed by classes outside the leveleditor.

class LevelData(object):
	"""docstring for LevelData"""
	def __init__(self, name, coords1, coords2, sunlit = False):
		self.name = name
		self.corners = (coords1, coords2)
		self.sunlit = sunlit #TODO: as level data gets more complicated, make this part of a more general set of tags.

	def room_set(self, rooms):
		room_set = []
		if self.corners[0] == None: return None
		corner1 = self.corners[0]
		corner2 = self.corners[1]
		for y in range(corner1[1], corner2[1] + 1):
			#room_set.append([]) #not sure if this would be useful
			for x in range(corner1[0],corner2[0]+1):
				room_set.append(rooms[y][x])
		return room_set

	def formatted_data(self): #used for saving to files
		return (self.name, self.corners[0], self.corners[1], self.sunlit)

	def setSunlit(self,sunlit):
		self.sunlit = sunlit

	@staticmethod
	def deformatted_level_set(formatted_data): #used for loading from files
		level_set = []
		for d in formatted_data:
			level_set.append(LevelData.deformatted_level(d))
		return level_set

	@staticmethod
	def deformatted_level(formatted_data): #used for loading from files
		return LevelData(formatted_data[0], formatted_data[1], formatted_data[2], formatted_data[3])