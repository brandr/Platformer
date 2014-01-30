import gameimage
from gameimage import *
import tile
from tile import *
import math
from math import *

class Entity(GameImage):
    def __init__(self,animations):#,default_rect = None,colorkey = None):
        GameImage.__init__(self,animations)#,default_rect,colorkey)
        self.color = BACKGROUND_COLOR
        self.unseen_color = Color("#FFFFFF")
        self.mapped = False
        self.current_level = None

    def dist_from(self,other):
        xdist = self.x_dist_from(other)
        ydist = self.y_dist_from(other)  
        xaligned = True
        yaligned = True
        if xdist >= ((self.rect.width/2) + (other.rect.width/2)):
            xaligned = False
        if ydist >= ((self.rect.height/2) + (other.rect.height/2)):
            yaligned = False
        if not xaligned:
            xdist -= ((self.rect.width/2) + (other.rect.width/2))
        if not yaligned:
            ydist -= ((self.rect.height/2) + (other.rect.height/2))
        return (math.sqrt(math.pow(xdist,2) + math.pow(ydist,2)))/32+0.0

    def x_dist_from(self,other,absolute = True):
        x1 = self.rect.centerx
        x2 = other.rect.centerx
        if(absolute):
            return abs(x2-x1)
        return x2-x1

    def y_dist_from(self,other,absolute = True):
        y1 = self.rect.centery
        y2 = other.rect.centery
        if(absolute):
            return abs(y2-y1)
        return y2-y1

    def withindist(self, other, dist):	#checks if the entity is close enough to another
        return self.dist_from(other) < dist

     #TODO: if outdoors, in the delete method there should be a call to the level to recalibrate shadows.
    def delete(self):
        self.currenttile().reset()      
        self.current_level.remove(self)    

    def currenttile(self):
        tiles = self.current_level.getTiles()
        coords = ((self.rect.topleft[0]+16)/32,(self.rect.topright[1] + 16)/32)
        return Tile.tileat(coords, tiles)

    def emit_light(self,dist,tiles,otherlights=None):
        starttile = self.currenttile()
        if not (starttile == None):
            starttile.emit_light(dist,tiles,otherlights)

    def darken_surf(self, amount):
        pass

    def calculate_brightness(self,coords):
        return 0

    def light_distance(self):
        return 0

    #might not end up using this method
    def castShadow(self):
        tiles = self.current_level.getTiles()
        start_tile = self.currenttile()
        if not (start_tile == None):
            down_shadow_tile = start_tile.relativetile((0,1),tiles)
            right_shadow_tile = start_tile.relativetile((1,0),tiles)
            if not (down_shadow_tile == None or down_shadow_tile.block != None):
                down_shadow_tile.castShadow(tiles,132)
            if not (right_shadow_tile == None or right_shadow_tile.block != None):
                right_shadow_tile.castShadow(tiles,168)

