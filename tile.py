import pygame
from pygame import Rect, Color, Surface
import math
from math import *
import gameimage
from gameimage import *

#OUTDOOR_SPRITE =  GameImage.loadImageFile('test_cave_tile_1.bmp',BACKGROUND_COLOR)
#TODO: implement sunlight

class Tile(GameImage):
    def __init__(self, tile_sprites, x , y): 
        GameImage.__init__(self,tile_sprites)#Rect(0, 0, 32, 32)) #TODO: replace with some getter (or arg) representing the tile's sprite.
        self.unseen_color = Color("#000000")
        self.rect = Rect(x, y, 32, 32)
        self.block = None
        self.mapped = False

    def changeImage(self,image = None):
        if(image != None):
            self.default_image = image
            self.image = image

    def reset(self):
        brightness = self.image.get_alpha()
        tile_image = self.default_image
        self.image = tile_image
        self.image.set_alpha(brightness)
        self.image.convert()
        self.block = None

    def updateimage(self, visible, lightvalue = 0):
        #print lightvalue
        if(self.block != None): 
            self.image = Surface((32,32))
            self.block.updateimage(lightvalue)
            return
        GameImage.updateimage(self,lightvalue)


    def darkenTo(self,lightvalue):
        GameImage.darkenTo(self,lightvalue)
        if(self.block != None): self.block.darkenTo(lightvalue)
    #emit_light: light is emitted in a circle from the tile, stopping at solid walls.

    def emit_light(self,dist,tiles,otherlights = []):
    	if otherlights != None:
    	    for o in otherlights:
    		    o.update_light(tiles)
        self.updateimage(True,256)
        directions = ((-1,0),(1,0),(0,-1),(0,1))
        for d in directions:
            nexttile = self.relativetile((d[0],d[1]),tiles)
            if nexttile != None:
                nexttile.spreadlight(dist-1, tiles, 1, (d[0],d[1]),False,None,otherlights)

    def spreadlight(self, dist, tiles, iteration = 0, direction = None, lineflag = False, brightness = None,otherlights = []):#might be more efficienct  ways to do this
        def get_brightness(): return ((0.9*dist+1)/(max(dist+iteration,1)))*256
        self.map()
        if brightness == None:
            brightness = get_brightness()
        maxbrightness = brightness
        if otherlights != None:
            for o in otherlights:
                if o.withindist(self, o.light_distance()):
                    checkbrightness = o.calculate_brightness(self.coordinates(),tiles)
                    maxbrightness = max(checkbrightness,brightness)
        self.updateimage(True,maxbrightness)  #update the current image based on light level
        if dist <= 0:
            return               #once the light reaches its max distance, stop
        if self.block!= None:
            d1 = (-1*direction[1],direction[0])
            d2 = (direction[1],-1*direction[0])
            nexttile1 = self.relativetile(d1,tiles)
            nexttile2 = self.relativetile(d2,tiles)
            if nexttile1 != None:
                nexttile1.spreadlight(0, tiles, iteration, d1, True, None, otherlights)
            if nexttile2 != None:
                nexttile2.spreadlight(0, tiles, iteration, d2, True, None, otherlights)           
            return
        starttile = self.relativetile(direction,tiles)
        if starttile != None:
            starttile.spreadlight(dist-1, tiles, iteration+1, direction, lineflag, None, otherlights)
        if lineflag: return
        #non-lineflag case (still going in one of the four intial directions)
        d1 = (-1*direction[1],direction[0])
        d2 = (direction[1],-1*direction[0])

        nexttile1 = self.relativetile(d1,tiles)
        nexttile2 = self.relativetile(d2,tiles)
        nextdist = math.sqrt(math.pow(iteration+dist - 1 ,2)-math.pow(iteration - 1,2))
        
        if nexttile1 != None:
            nexttile1.spreadlight(nextdist, tiles, iteration+1, d1, True, None, otherlights)  
        if nexttile2 != None:
            nexttile2.spreadlight(nextdist, tiles, iteration+1, d2, True, None, otherlights)

    def castShadow(self, tiles, brightness):
        pass
        #self.darkenTo(brightness)
        #if(brightness >= 256 or self.block != None):return
        #down_tile = self.relativetile((0,1),tiles)
        #right_tile = self.relativetile((1,0),tiles)
        #if not (down_tile == None):
        #    down_tile.castShadow(tiles,brightness*1.06)
        #if not (right_tile == None):
        #    right_tile.castShadow(tiles,brightness*1.06)
 
    def relativetile(self,coords,tiles):
        startcoords = self.coordinates()
        tilecoords = (startcoords[0] + coords[0], startcoords[1] + coords[1])
        if Tile.validcoords(tilecoords,tiles): #this check might not be necessary here
        	return Tile.tileat((tilecoords[0],tilecoords[1]),tiles)
        return None

    def coordinates(self):
    	return (self.rect.centerx/32,self.rect.centery/32)

    def map(self):
        self.mapped = True 
        if(self.block != None):
            self.block.mapped =True

    @staticmethod
    def validcoords(coords,tiles): #checks if a set of tile coords correspond to an actual tile on the level.
        if(coords == None or coords[0] == None or coords[1] == None):
        	return False
    	minuscheck = coords[0] >= 0 and coords[1] >= 0
        ymax = len(tiles)
        xmax = len(tiles[0])
    	pluscheck = coords[0] < xmax and coords[1] < ymax
    	return minuscheck and pluscheck

    @staticmethod
    def tileat(coords,tiles):	#the tile on the level at a set of coords
        if(Tile.validcoords(coords,tiles)):
            return tiles[coords[1]][coords[0]]
        return None