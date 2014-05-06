from camera import *
from levelobjects import *
from gameimage import *


class Room(object):
	#ROOM_WIDTH = LevelObjects.ROOM_WIDTH
	#ROOM_HEIGHT = LevelObjects.ROOM_HEIGHT
	def __init__(self, level_objects,dungeon,global_coords,start_coords):
		tiles = level_objects.get_tiles()
		self.level_objects = level_objects
		self.global_coords = global_coords
		self.start_coords = start_coords
		self.dungeon = dungeon

	def calibratePositions(self,level_origin):
		x_offset = 32*(self.global_coords[0] - level_origin[0])
		y_offset = 32*(self.global_coords[1] - level_origin[1])
		self.level_objects.calibratePositions(x_offset,y_offset)

	def setLevel(self,level): #if it's useful, actually store the level as a data member.
		self.level_objects.setLevel(level)

	def entities_to_string(self): #for testing
		dimensions = (ROOM_WIDTH,ROOM_HEIGHT)
		entities_string_array = []
		while(len(entities_string_array)<=dimensions[1]):
			entities_string_array.append([])
		for s in entities_string_array:
			while len(s)<=dimensions[0]:
				s.append(" ")
		entities = self.level_objects.get_entities(Entity)
		for e in entities:
			coords = (e.rect.centerx/32,e.rect.centery/32)
			entities_string_array[coords[1]][coords[0]] = "E"
		entities_string = ""
		for y in range(0,dimensions[1]):
			for x in range(0,dimensions[0]):
				entities_string += entities_string_array[y][x]
			entities_string += "\n"
		return entities_string
