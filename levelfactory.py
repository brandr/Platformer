import tilefactory
from tilefactory import *
import platformfactory
from platformfactory import *
import level
from level import *
import lantern
from lantern import *
import exitblock
from exitblock import *
import monster
from monster import *

class LevelFactory(object):

	#ROOM_WIDTH = 32
	#ROOM_HEIGHT = 16

	def __init__(self):
		self.global_x = 0
		self.global_y = 0


	#maybe this should go in roomfactory instead

	def dungeon_rooms(self,dungeon,dungeon_map):
		ROOM_WIDTH = Room.ROOM_WIDTH
		ROOM_HEIGHT = Room.ROOM_HEIGHT
		rooms = []
		map_width = len(dungeon_map[0])
		map_height = len(dungeon_map)
		rooms_x = map_width/ROOM_WIDTH   #assuming evenly divisible right now
		rooms_y = map_height/ROOM_HEIGHT
		for y in range(0,rooms_y):	#NOTE: this for loop seems to obviate the need for global coords.
			rooms.append([])
			for x in range(0,rooms_x):
				next_room = self.build_room(dungeon,dungeon_map,x,y)
				rooms[y].append(next_room)
		return rooms

	def build_room(self,dungeon,dungeon_map,global_x,global_y):
		tiles = []
		entities = [] #figure out why the original platformer used Group

		start_coords = (False,0,0)
		x = y = 0

		tile_images = GameImage.loadImageFile('test_tiles_1.bmp') 
		tile_factory = TileFactory(tile_images, (2,1))
		default_cave_tile = tile_factory.tile_at((0,0))
		default_sky_tile = tile_factory.tile_at((1,0))
		default_tile = default_cave_tile
		default_platform_image = GameImage.loadImageFile('testblock1.bmp')
		default_platform = GameImage.still_animation_set(default_platform_image)
		default_lantern = Lantern.load_lantern_animation_set()
		default_bat = Monster.load_bat_animation_set() 

		map_width = len(dungeon_map[0])
		map_height = len(dungeon_map)

		#NOTE: there might be some way to derive x and y from other values,
			  #rather than by taking them as args.
		start_x = global_x*Room.ROOM_WIDTH
		start_y = global_y*Room.ROOM_HEIGHT

		end_x = min(start_x+Room.ROOM_WIDTH,map_width)
		end_y = min(start_y+Room.ROOM_HEIGHT,map_height)

		for row in range(start_y,end_y):
			tiles.append([])
			for col in range(start_x,end_x):
				t = Tile(default_tile, x,y)
				#if dungeon_map[y/32][x/32] == "P":
				if dungeon_map[row][col] == "P":
					p = Platform(default_platform, x, y)
					entities.append(p)
					t.block = p
				if dungeon_map[row][col] == "L":
					l = Lantern(default_lantern, x, y, 2)
					entities.append(l)
				if dungeon_map[row][col] == "S":
					start_coords = (True,x,y)
				if dungeon_map[row][col] == "B":
					#print ((global_x,global_y),"monster",x,y)
					b = Monster(default_bat,"bat",x,y)
					entities.append(b)
				tiles[y/32].append(t)
				x += 32 
			y += 32
			x = 0

		room_objects = LevelObjects(None,tiles,entities)
		created_room = Room(room_objects,dungeon,(global_x,global_y),start_coords)
		#print (global_x,global_y)
		#monsters = created_room.level_objects.get_entities(Monster)
		#for m in monsters: print "B"
		#TODO: increment global coords accordingly (or not?)
		return created_room

	def dungeon_levels(self,dungeon,rooms,level_data):
		levels = []
		#TODO:conisder making level_data its own class (to make this more extensible)
		for d in level_data:
			level_ID = d[0]
			origin = d[1]
			room_coords = d[2]
			level_rooms = []
			for c in room_coords: #TODO: error checking
				next_room = rooms[c[1]][c[0]]
				level_rooms.append(next_room)
			next_level = self.build_level(dungeon,level_ID,origin,level_rooms)
			#print next_level.level_ID
			#monsters = next_level.level_objects.get_entities(Monster)
			#for m in monsters: print "B"
			levels.append(next_level)
		return levels

		#If I end up using the system where levelIDs are stored in arrays corresponding to rooms,
			#should probably have this done for dungeon in this method.
	def build_level(self,dungeon,level_ID,origin,rooms):
		return Level(dungeon,level_ID,origin,rooms)

		#NOTE: this method is outdated and will almost definitely be completely deleted.
	def newLevel(self, level_map, global_coords,dungeon):
			
			tiles = []
			platforms = []
			lanterns = []
			monsters = []

			entities = pygame.sprite.Group()

			start_coords = (False,0,0)
			linked_levels = []

			x = y = 0
			#rowindex = 0

			#this part can probably be done more extensibly, probably by reading in an image to go with the level
			#could store the image/level object map in one data structure and read this in instead of the level map.
			#long term idea: build levels using preset tiles in a map editor, then tweak the resulting images in pinta.
			tile_images = GameImage.loadImageFile('test_tiles_1.bmp') 

			tile_factory = TileFactory(tile_images, (2,1))

			default_cave_tile = tile_factory.tile_at((0,0))
			default_sky_tile = tile_factory.tile_at((1,0))

			default_tile = default_cave_tile

			default_platform_image = GameImage.loadImageFile('testblock1.bmp')
			default_platform = GameImage.still_animation_set(default_platform_image)

			default_lantern = Lantern.load_lantern_animation_set()

			default_bat = Monster.load_bat_animation_set() #TEMPORARY

			if(self.outdoors(global_coords[1],level_map[0])):
				default_tile = default_sky_tile

			for row in level_map:
				tiles.append([])
				for col in row:
					t = Tile(default_tile, x,y) #should sort these in order of frequency (most-least). Also, what the hell did I mean when I wrote that?
					if col == "P":
						p = Platform(default_platform, x, y)
						platforms.append(p)
						entities.add(p)
						t.block = p
					if col == "L":
						l = Lantern(default_lantern, x, y, 2)
						platforms.append(l)
						lanterns.append(l)
						entities.add(l)
					if col == "N": #N for "next"
						e = ExitBlock(default_platform, x, y) #temp since there's no sprite anyway
						platforms.append(e)
						entities.add(e)
						t.block = e
					if col == "S":
						start_coords = (True,x,y)
					#TEMPORARY
					if col == "B":
						b = Monster(default_bat,"bat",x,y)
						monsters.append(b)
						entities.add(b)
					#TEMPORARY
					tiles[y/32].append(t)
					x += 32 
				y += 32
				x = 0

			return Level(tiles,entities,platforms,monsters,lanterns,dungeon,global_coords,start_coords) 

	def outdoors(self,depth,level_top):
		if(depth > 0): return False
		width = len(level_top)
		blocked = 0
		for t in level_top:
			if (t != " "): #should really be transparency check
				blocked += 1
		return blocked < width/1.5