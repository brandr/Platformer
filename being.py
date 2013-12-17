import entity
from entity import *

#a being is an entity that does not occupy a specific tile (like a block/platform does).
#beings can be stationary, though they almost always move.

class Being(Entity):
    def __init__(self,animations):
        Entity.__init__(self,animations)
        #TODO: if methods/data from monster/player are universal, move them to this class.