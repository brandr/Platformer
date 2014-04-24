from block import *

class Platform(Block):
    def __init__(self, animations, x, y):
        Block.__init__(self, animations, x, y)

    def update(self, player):	
        pass

    def darkenTo(self, lightvalue):
        self.image = self.default_image
        current_lightvalue = self.image.get_alpha()
        self.image.set_alpha(min(current_lightvalue, lightvalue))