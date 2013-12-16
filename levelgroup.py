import levelfactory
from levelfactory import *
import player
from player import *

class LevelGroup(object):
	def __init__(self,levels):
		global_x = 0
		global_y = 0
		self.levels = []
		factory = LevelFactory()
		for row in levels:
			self.levels.append([])
			for L in row:
				next_level = factory.newLevel(L,(global_x, global_y),self)
				self.levels[global_y].append(next_level)
				global_x += 1
			global_y += 1
			global_x = 0

	def start_level(self):
		for row in self.levels:
			for L in row:
				if(L.start_coords != None):
					return L
		return None

	def movePlayer(self,player,global_coords,direction):
		x_coord = global_coords[0] + direction[0]
		y_coord = global_coords[1] + direction[1]
		next_level = self.levels[y_coord][x_coord]
		current_coords = player.currenttile().coordinates()
		next_coords = next_level.flipped_coords(current_coords)
		next_level.addPlayer(player,next_coords)
		