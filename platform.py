import entity
from entity import *

class Platform(Entity):
    def __init__(self, animations, x, y):
        Entity.__init__(self,animations)
        self.unseen_color = Color("#FFFFFF") #TODO: need "unseen image" instead
        self.rect = Rect(x, y, 32, 32)
        self.is_sloped = False

    def update(self, player):	
        pass

    def updateimage(self, lightvalue = 0):#visible arg was removed
    	if(lightvalue != 0): 
            self.image = self.default_image 
            self.image.set_alpha(lightvalue)
        else: 
            self.image = Surface((32, 32)) #TODO: consider making the unseen image a const value that 
            if(self.mapped):    #both platforms and tiles can access (or private data if it should vary)
                self.image.fill(self.unseen_color)    #same for unseen color
                self.image.set_alpha(16)
                return
            self.image.fill(BACKGROUND_COLOR)

    def darkenTo(self, lightvalue):
        self.image = self.default_image
        current_lightvalue = self.image.get_alpha()
        self.image.set_alpha(min(current_lightvalue, lightvalue))