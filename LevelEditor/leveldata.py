#NOTE: this class might need to be accessed by classes outside the leveleditor.

class LevelData(object):
	"""docstring for LevelData"""
	def __init__(self,name,coords1,coords2):
		self.name = name
		self.corners = (coords1,coords2)

	def room_set(self,rooms):
		room_set = []
		corner1 = self.corners[0]
		corner2 = self.corners[1]
		for y in range(corner1[0],corner1[1]+1): #not sure if +1 is correct or not
			#room_set.append([]) #not sure if this would be necessary/useful
			for x in range(corner2[0],corner2[1]+1):
				room_set.append(rooms[y][x])
		return room_set

	def formatted_data(self): #used for saving to files
		return (self.name,self.corners[0],self.corners[1])

	@staticmethod
	def deformatted_level_set(formatted_data): #used for loading from files
		level_set = []
		for d in formatted_data:
			level_set.append(LevelData.deformatted_level(d))
		return level_set

	@staticmethod
	def deformatted_level(formatted_data): #used for loading from files
		return LevelData(formatted_data[0],formatted_data[1],formatted_data[2])