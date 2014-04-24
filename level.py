from room import *
from roomfactory import *
from tilefactory import * #TEMPORARY IMPORT

class Level(object):
	#a level is built from a rectangular set of rooms.
	#it copies all objects from the rooms into itself, and processes these objects as the game is running.
	#only the player's current level should be active at any given time
	def __init__(self, dungeon, level_data, origin, rooms):
		self.screen = None
		self.dungeon = dungeon 		#the LevelGroup that the level is part of
		self.level_ID = level_data.name #a currently unused value which identifies the level uniquely
		self.origin = origin 	#upper-left corner of the level (in terms of global coords, so each coordinate pair corresponds to a room)
		self.level_objects = LevelObjects(self) #all objects in the level (tiles and entities)
		self.start_coords = None #coords where the player appears upon entering the level (set by addRooms)
		self.addRooms(rooms)
		tiles = self.getTiles()
		self.width = len(tiles[0])
		self.height = len(tiles)
		total_level_width = self.width*32
		total_level_height = self.height*32
		self.level_camera = Camera(total_level_width, total_level_height) #might not be the best way to make the camera
		self.outdoors = level_data.sunlit

		if(self.outdoors): self.setTilesOutdoors() #TEMP
		
		self.calibrateLighting()

		#toString test methods
	def to_string(self): #will only be used for testing, I  think
		level_string = ""
		tiles = self.getTiles()
		for row in tiles:
			for t in row:
				if t.block != None:
					level_string += "P"
				else:
					level_string += " "
			level_string += "\n"
		return level_string

	def entities_to_string(self): #for testing
		dimensions = self.get_dimensions()
		entities_string_array = []
		while(len(entities_string_array) <= dimensions[1]):
			entities_string_array.append([])
		for s in entities_string_array:
			while len(s) <= dimensions[0]:
				s.append(" ")
		entities = self.getEntities()
		for e in entities:
			coords = (e.rect.left/32, e.rect.right/32)
			entities_string_array[coords[1]][coords[0]] = "E"
		entities_string = ""
		for y in range(0, dimensions[1]):
			for x in range(0, dimensions[0]):
				entities_string += entities_string_array[y][x]
			entities_string += "\n"
		return entities_string

		#TEMP METHOD
	def setTilesOutdoors(self):
		default_sky_tile = GameImage.load_image_file('./data/', 'test_sky_tile_1.bmp') #GameImage.loadImageFile('test_sky_tile_1.bmp') 
		dimensions =  self.get_dimensions()
		tiles = self.getTiles()
		for y in xrange(dimensions[1]):
			for x in xrange(dimensions[0]):
				tiles[y][x].changeImage(default_sky_tile) #Tile(default_sky_tile, x,y)
		#TEMP METHOD

		#level building methods (called in constructor)
	def addRooms(self, rooms):
		for r in rooms:
			level_objects = r.level_objects
			self.level_objects.addLevelObjects(r.global_coords, level_objects)
			self.setStartCoords(r)

	def setStartCoords(self, room):
		if self.start_coords != None: return
		if room.start_coords[0]:
			self.start_coords = (room.start_coords[1], room.start_coords[2])
			return

	#outdoor-related methods
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
				t.fullyDarken()
	
		#if any exits to the level don't lead anywhere, add blocks barring the player from leaving.
	def calibrateExits(self):
		tiles = self.getTiles()
		x_tiles = len(tiles[0]) - 1
		y_tiles = len(tiles) - 1
		exit_tiles = []

		for t in tiles[0]: #ceiling
			if(t.passable()):
				exit_tiles.append((t,(0,-1)))
		for t in tiles[y_tiles]: #floor
			if(t.passable()):
				exit_tiles.append((t,(0,1)))
		for row in tiles: #walls
			if(row[0].passable()): #left wall
				exit_tiles.append((row[0],(-1,0)))
			if(row[x_tiles].passable()): #right wall
				exit_tiles.append((row[x_tiles],(1,0)))
		for e in exit_tiles:
			tile = e[0]
			direction = e[1]
			x = tile.coordinates()[0]
			y = tile.coordinates()[1]
			if self.next_level_exists(self.global_coords((x, y)), direction): #this is the sort of area whre we want to get rid of these 32s
				continue
			exit_platform_image = GameImage.load_image_file('./data/', 'exitblock1.bmp') #TODO: make exitblocks more terrifying in case anyone finds them
			exit_platform = GameImage.still_animation_set(exit_platform_image) #TEMPORARY
			block_x = 32*(x + direction[0])
			block_y = 32*(y + direction[1])
			self.level_objects.addBlock(Platform(exit_platform, block_x, block_y))

		#directonal/movement methods

	def level_in_direction(self, global_x, global_y, direction): #doesn't really need anything from this level in particular, but this method works here for now
		x_coord = global_x + direction[0]
		y_coord = global_y + direction[1]
		return self.dungeon.level_at(x_coord,y_coord)

		#find the direction of the level a tile is in, assuming that it is outside this level's borders.
	def direction_of(self,coords):
		dimensions = self.get_dimensions()
		if(coords[0] <= 1): return (-1, 0)
		if(coords[0] >= dimensions[0] - 1): return (1, 0)
		if(coords[1] <= 1): return (0, -1)
		if(coords[1] >= dimensions[1] - 1): return (0, 1)
		return (0,0)

	def global_coords(self,position):
		min_x = self.origin[0]
		min_y = self.origin[1]
		x_offset = position[0]/ROOM_WIDTH
		y_offset = position[1]/ROOM_HEIGHT
		return (min_x+x_offset, min_y+y_offset)

	def flipped_coords(self,global_coords,local_coords):
		dimensions = self.get_dimensions()
		origin_x = self.origin[0]

		if(local_coords[0] <= 1):				# left edge of level
			return (dimensions[0] - 2, local_coords[1])		
		if(local_coords[0] >= ROOM_WIDTH - 2):	# right edge of level
			return (2, local_coords[1])
		if(local_coords[1] <= 1):				# top edge of level
			return (local_coords[0],dimensions[1] - 2)
		if(local_coords[1] >= ROOM_HEIGHT - 2):	# bottom edge of level
			return (local_coords[0], 2)
		#TODO: error case (no possible edge detected for exitblock)

	def next_level_exists(self, global_coords, direction):
		next_level = self.level_in_direction(global_coords[0], global_coords[1], direction)
		return next_level != None

	def movePlayer(self, coords):
		player = self.getPlayer()
		direction = self.direction_of(coords)
		adjusted_coords = (coords[0] - direction[0], coords[1] - direction[1])
		self.removePlayer()
		global_coords = self.global_coords(adjusted_coords)
		if(self.next_level_exists(global_coords, direction)):
			next_level = self.level_in_direction(global_coords[0], global_coords[1], direction)
			self.dungeon.movePlayer(self.screen, player, next_level, global_coords, adjusted_coords)
		#TODO: error case

	def addPlayer(self, player, coords = None):
		player.current_level = self
		self.level_objects.addPlayer(player)
		if(coords == None):	
			player.moveRect(self.start_coords[0], self.start_coords[1], True)
			return
		player.moveTo(coords)
		self.level_camera.update(player)
		player.update(self.getTiles(), False, False, False, False, False)
		pygame.display.update()

#TODO: could put up,down,left,right and running into a single object which describes the player's current state
	def update(self, up, down, left, right, running):	
		player = self.getPlayer()
		all_tiles = self.getTiles()
		start_x = max(0, self.level_camera.state.left/32)
		end_x = min(self.level_camera.state.right/32, self.width)
		start_y = max(0, self.level_camera.state.top/32)
		end_y = min(self.level_camera.state.bottom/32, self.height)
		tiles = all_tiles[start_y:end_y][start_x:end_x]
		if(player != None):
			self.level_camera.update(player)
			player.update(all_tiles, up, down, left, right, running)
			platforms = self.getPlatforms()
			#for p in platforms: #not sure this is necessary. may use it later.
			#	p.update(player)	
			for row in tiles:
				for t in row:
					self.screen.blit(t.image, self.level_camera.apply(t))
			for e in self.getEntities():
				self.screen.blit(e.image, self.level_camera.apply(e))
			pygame.display.update()

	def level_end_coords(self):
		tiles = self.getTiles()
		width  = len(tiles[0]) - 1
		height = len(tiles) - 1
		return (self.origin[0] + (width/ROOM_WIDTH),self.origin[1] + (height/ROOM_HEIGHT))

	def get_dimensions(self):
		tiles = self.getTiles()
		width  = len(tiles[0])
		height = len(tiles)
		return (width, height)

	def remove(self,entity):
		self.level_objects.remove(entity)
		if(self.outdoors): self.calibrateLighting()

	def getTilesOnScreen(self):
		all_tiles = self.getTiles()
		return self.level_camera.on_screen_tiles(all_tiles)

	def removePlayer(self):
		self.level_objects.removePlayer()

	def getPlayer(self):
		return self.level_objects.player

	def getTiles(self):
		return self.level_objects.tiles

	def getEntities(self):
		return self.level_objects.get_entities(Entity)
		
	def getPlatforms(self):
		return self.level_objects.get_entities(Platform)

	def getLadders(self):
		return self.level_objects.get_entities(Ladder)
		
	def getMonsters(self):
		return self.level_objects.get_entities(Monster)

	def getLanterns(self):
		return self.level_objects.get_entities(Lantern)

	def get_exit_blocks(self):
		return self.level_objects.get_entities(ExitBlock)
		