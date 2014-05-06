from entity import *

class Lantern(Entity):	#lantern which can help the player see
    def __init__(self, animations, x, y, lightvalue = 2):
        Entity.__init__(self,animations)
        self.rect.centerx += x
        self.rect.centery += y
        self.lightvalue = lightvalue
        self.animated = True

    def update(self, player):
        self.updateAnimation() 

    def update_light(self, tiles):
        self.emit_light(self.lightvalue, tiles)

    def calculate_brightness(self, coords, tiles):
    	other = Tile.tileat(coords,tiles)
    	temp_dist = max(1, self.dist_from(other))
    	temp_dist = max(0, self.lightvalue - temp_dist + 1)
    	temp_brightness = ((0.9*temp_dist)/(self.lightvalue))*256
        return min(temp_brightness, 255)

    def light_distance(self):
    	return self.lightvalue