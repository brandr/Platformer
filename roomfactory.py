from tilefactory import *
from platformfactory import *
from level import *
from lantern import *
from exitblock import *
from monster import *
import sys
sys.path.insert(0, './LevelEditor')
from roomdata import *

class RoomFactory(object):

	@staticmethod
	def dungeon_rooms(dungeon,room_data_set):
		rooms = []
		x1,y1 = RoomFactory.origin(room_data_set)
		x2,y2 = RoomFactory.lower_right(room_data_set)
		print "Setting up rooms..."
		for y in range(y1,y2+1):	#NOTE: this for loop seems to obviate the need for global coords.
			rooms.append([])
			for x in range(x1,x2+1):
				next_data = room_data_set[y][x]
				next_room = RoomFactory.build_room(dungeon,next_data,x,y)
				rooms[y].append(next_room)
		print "Rooms set up."
		return rooms

	@staticmethod
	def origin(room_data_set):
		for y in xrange(len(room_data_set)):
			for x in xrange(len(room_data_set[y])):
				next_data = room_data_set[y][x]
				if(room_data_set[y][x] != None):return x,y
		return None

	@staticmethod
	def lower_right(room_data_set):
		for y in range(len(room_data_set)-1,-1,-1):
			for x in range(len(room_data_set[y])-1,-1,-1):
				next_data = room_data_set[y][x]
				if(room_data_set[y][x] != None):return x,y
		return None

	@staticmethod
	def build_room(dungeon,room_data,global_x,global_y): #might be able to get global x and global y through roomdata's coords instead
		if(room_data == None): return RoomFactory.empty_room(dungeon,global_x,global_y) 
		tiles = []
		entities = [] #TODO: figure out why the original platformer used Group

		start_coords = (False,0,0)
		x = y = 0
		#global_x,global_y = room_data.global_x,room_data.global_y #probably redundant

		tile_images = GameImage.loadImageFile('test_tiles_1.bmp') 
		tile_factory = TileFactory(tile_images, (2,1))
		default_cave_tile = tile_factory.tile_at((0,0))
		default_tile = default_cave_tile

		default_lantern = Lantern.load_lantern_animation_set()	#TEMP
		

		end_x = ROOM_WIDTH
		end_y = ROOM_HEIGHT

		for row in xrange(end_y):
			tiles.append([])
			for col in xrange(end_x):
				next_tile_data = room_data.tile_at(col,row)
				t = Tile(default_tile, x,y)
				if next_tile_data != None and not isinstance(next_tile_data,BlockedTileData):
				#TODO: think of a more extensible way to build these objects (probably through dictionaries or something)
				#IDEA: make PLAYER_START its own case, but make everything else create an object fetched via a dictionary.
				#TODO: remember also that this part will need some checks if the object created is larger than 32*32.
					raw_entity_image = next_tile_data.get_image("./LevelEditor")
					entity_width, entity_height = next_tile_data.width, next_tile_data.height
					entity_rect = Rect(0,0,entity_width*DEFAULT_TILE_SIZE,entity_height*DEFAULT_TILE_SIZE)
					still_entity_image = GameImage.still_animation_set(raw_entity_image,entity_rect)

					#IDEA: give Entity a map of entity keys to animation sets

					#TODO: could save a lot of time by checking whether the entity is animated first.
					#entity_animation_set = next_tile_data.get_animation_set("./LevelEditor")
					if next_tile_data.entity_key == DEFAULT_PLATFORM:
						p = Platform(still_entity_image, x, y)	#TODO: use still entity image here (I think)
						entities.append(p)
						t.block = p
					if next_tile_data.entity_key == PLAYER_START:
						start_coords = (True,x,y)
					if next_tile_data.entity_key == BAT:
						default_bat = Monster.load_bat_animation_set() #TEMP
						b = Monster(default_bat,"bat",x,y)
						entities.append(b)
					if next_tile_data.entity_key == GIANT_FROG:
						default_frog = Monster.load_giant_frog_animation_set() #TEMP
						f = Monster(default_frog,"giant frog",x,y) #TODO: make it possible to animate giant frog, and extensibly load animations.
						entities.append(f)
				#if dungeon_map[row][col] == "L": #TODO: lantern
				#	l = Lantern(default_lantern, x, y, 2)
				#	entities.append(l)
				tiles[y/32].append(t)
				x += 32 
			y += 32
			x = 0

		room_objects = LevelObjects(None,tiles,entities)
		created_room = Room(room_objects,dungeon,(global_x,global_y),start_coords)
		return created_room

	@staticmethod
	def empty_room(dungeon,global_x,global_y):
		tiles = []
		entities = []

		start_coords = (False,0,0)
		x = y = 0

		tile_images = GameImage.loadImageFile('test_tiles_1.bmp') 
		tile_factory = TileFactory(tile_images, (2,1))
		default_cave_tile = tile_factory.tile_at((0,0))
		default_sky_tile = tile_factory.tile_at((1,0))
		default_tile = default_cave_tile

		end_x = ROOM_WIDTH
		end_y = ROOM_HEIGHT

		for row in xrange(end_y):
			tiles.append([])
			for col in xrange(end_x):
				t = Tile(default_tile, x,y)
				tiles[y/32].append(t)
				x += 32 
			y += 32
			x = 0

		room_objects = LevelObjects(None,tiles,entities)
		created_room = Room(room_objects,dungeon,(global_x,global_y),start_coords)
		return created_room