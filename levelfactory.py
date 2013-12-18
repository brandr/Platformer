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

	def newLevel(self, level_map, global_coords,dungeon):
			
			tiles = []
			platforms = []
			lanterns = []
			monsters = []

			entities = pygame.sprite.Group()

			start_coords = (False,0,0)
			linked_levels = []

			x = y = 0
			rowindex = 0

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