import pygame
from pygame import *
import camera
from camera import *
import levelobjects
from levelobjects import *
import gameimage
from gameimage import *

class Level(object):
	#NOTE: this is a lot of args. May want to put them in levelObjects before creating the level, not after.
	def __init__(self, tiles,entities,platforms,monsters,lanterns,dungeon,global_coords,start_coords):#,outdoors = True):
		total_level_width  = len(tiles[0])*32
		total_level_height = len(tiles)*32
		self.level_camera = Camera(total_level_width, total_level_height)	
		self.level_objects = LevelObjects(self,tiles,entities,platforms,monsters,lanterns)
		self.global_coords = global_coords
		self.start_coords = None
		self.setStartCoords(start_coords)
		self.dungeon = dungeon
		self.outdoors = self.outdoors() #TODO: take this as an arg from the factory
		self.calibrateLighting()

	def setStartCoords(self, start_coords):
		if(start_coords[0]):
			self.start_coords = (start_coords[1],start_coords[2])

	def outdoors(self):
		if(self.global_coords[1] > 0): return False
		tiles = self.getTiles()
		width = len(tiles[0])
		blocked = 0
		for t in tiles[0]:
			if (t.block != None): #should really be transparency check
				blocked += 1
		return blocked < width/1.5

	def	calibrateLighting(self):
		if(self.outdoors): #TODO: separate this into its own method
			tiles = self.getTiles()
			for row in tiles:
				for t in row:
					t.changeImage()
					t.updateimage(256)
			return
		tiles = self.getTiles()
		for row in tiles:
			for t in row:
				t.updateimage()

	def direction_of(self,exit_block):
		dimensions = self.get_dimensions()
		exit_tile = exit_block.currenttile()
		tile_coordinates = exit_tile.coordinates()
		if(tile_coordinates[0] <= 1): return (-1,0)
		if(tile_coordinates[0] >= dimensions[0] - 1): return (1,0)
		if(tile_coordinates[1] <= 1): return (0,-1)
		if(tile_coordinates[1] >= dimensions[1] - 1): return (0,1)
		return (0,0)

	def flipped_coords(self,coords):
		dimensions = self.get_dimensions()
		if(coords[0] <= 1):
			return (dimensions[0] - 2, coords[1])		
		if(coords[0] >= dimensions[0] - 3):
			return (2, coords[1])
		if(coords[1] <= 1):
			return (coords[0],dimensions[1] - 2)
		if(coords[1] >= dimensions[1] - 3):
			return (coords[0],2)
		#TODO: error case (no possible edge detected for exitblock)

	def movePlayer(self,exit_block):
		player = self.getPlayer()
		direction = self.direction_of(exit_block)
		self.removePlayer()
		self.dungeon.movePlayer(player,self.global_coords,direction)

	def addPlayer(self,player,coords = None):
		player.current_level = self
		self.level_objects.addPlayer(player)
		if(coords == None):	
			player.rect = Rect(self.start_coords[0], self.start_coords[1], 32, 64) #TODO: get size from player's image instead
			return
		player.moveTo(coords)
		self.level_camera.update(player)
		player.update(False,False,False,False,False)
		pygame.display.update()

#TODO: could put up,down,left,right and running into a single object which describes the player's current state
	def update(self,screen,up, down, left, right, running):	
		player = self.getPlayer()
		if(player != None):
			self.level_camera.update(player)
			player.update(up, down, left, right, running)
			platforms = self.getPlatforms()
			for p in platforms: #not sure this is necessary
				p.update(player)
			for row in self.getTiles():
				for t in row:
					screen.blit(t.image, self.level_camera.apply(t))
			for e in self.getEntities():
				screen.blit(e.image, self.level_camera.apply(e))

			pygame.display.update()

	def get_dimensions(self):
		tiles = self.getTiles()
		width  = len(tiles[0])
		height = len(tiles)
		return (width,height)

	def remove(self,entity):
		self.level_objects.remove(entity)
		if(self.outdoors): self.calibrateLighting()

	def removePlayer(self):
		self.level_objects.removePlayer()

	def getPlayer(self):
		return self.level_objects.player

	def getTiles(self):
		return self.level_objects.tiles

	def getEntities(self):
		return self.level_objects.entities
		
	def getPlatforms(self):
		return self.level_objects.platforms
		
	def getMonsters(self):
		return self.level_objects.monsters

	def getLanterns(self):
		return self.level_objects.lanterns
		