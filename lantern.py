from entity import *

FLICKER_CONSTANT = 80

class Lantern(Entity):	#lantern which can help the player see
    def __init__(self, animations, x, y):
        Entity.__init__(self, animations)
        self.rect.centerx += x
        self.rect.centery += y
        self.animated = True
        self.flicker_index = 0

        # TODO: figure out a good oil system
        self.oil_meter = [3999, 3999]
        self.light_multiplier = 4

    def update(self, player):
        self.flicker_update()
        self.updateAnimation()

    def oil_update(self):
        self.flicker_update()
        if self.oil_meter[0] > 0:
            self.oil_meter[0] -= 1

    def flicker_update(self):
        self.flicker_index += 1
        if self.flicker_index >= FLICKER_CONSTANT: self.flicker_index = 0

    def light_distance(self): #may have different lantern with different light functions for different gameplay
        if not self.oil_meter[0]:
            return 0
        oil_ratio = float(self.oil_meter[0])/float(self.oil_meter[1])
        distance = int(oil_ratio*self.light_multiplier)
        if self.flicker_index < FLICKER_CONSTANT/2:
            distance -= 1 
        return distance

    def update_light(self, tiles, light_map):
        light_distance = self.light_distance()
        self.emit_light(light_distance, tiles, light_map)

    def add_oil(self, oil_value):
        self.oil_meter[0] = min(self.oil_meter[0] + oil_value, self.oil_meter[1])

    def is_empty(self):
        return self.oil_meter[0] <= 0 

    def calculate_brightness(self, coords, tiles):
        other = Tile.tileat(coords,tiles)
        temp_dist = max(1, self.dist_from(other))
        temp_dist = max(0, self.lightvalue - temp_dist + 1)
        temp_brightness = ((0.9*temp_dist)/(self.lightvalue))*256
        return min(temp_brightness, 255)