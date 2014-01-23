import entity
from entity import *

#a being is an entity that does not occupy a specific tile (like a block/platform does).
#beings can be stationary, though they almost always move.

class Being(Entity):
    def __init__(self,animations):
        Entity.__init__(self,animations)
        self.direction_id = None
        self.xvel = 0
        self.yvel = 0
        self.mobile = True
        self.onGround = False
        self.running = False
        self.sightdist = 5
        self.max_speed = 10 #doesn't apply to player yet, but could
        self.bounce_count = 0
        #TODO: if methods/data from monster/player are universal, move them to this class.

    def updateAnimation(self, light_value = None): #differs from usual updateImage in that we must find this being's current tile because it can change a lot.
        if self.currenttile() == None: return
        if(light_value == None):
            light_value = self.currenttile().check_brightness()
        #IDEA: if light value is 0 at this point, set the animation either to complete darkness or to some "darkened" animation. 
        #(i.e., the bat's darkened animation appears only as two red eyes. )
        GameImage.updateAnimation(self, light_value)

    def updatePosition(self):
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel)

    #TODO: consider having bounce take effect here, like in player.
    def collide(self, xvel, yvel, collide_objects = None):
        if(collide_objects == None):
            level = self.current_level
            collide_objects = level.getPlatforms()
        for c in collide_objects:
            self.collideWith(xvel,yvel,c)

    def collideWith(self,xvel,yvel,collide_object):
        if pygame.sprite.collide_rect(self, collide_object):
                if xvel > 0:
                    self.rect.right = collide_object.rect.left
                if xvel < 0:
                    self.rect.left = collide_object.rect.right
                if yvel > 0:
                    self.rect.bottom = collide_object.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = collide_object.rect.bottom

    def moveTowards(self,destination):
        if self.bounce_count > 0:
            self.bounce()
            return 
        distance = self.dist_from(destination)
        if(distance == 0): return
        dist_ratio = self.max_speed/distance
        self.xvel = dist_ratio*self.x_dist_from(destination,False)/32
        self.yvel = dist_ratio*self.y_dist_from(destination,False)/32

    def bounceAgainst(self,other): #this is used for a monster colliding with the player, and may be useful in other cases.
    	if(self.bounce_count > 0): return
        x_direction_sign = 1
        y_direction_sign = 1
        if(self.rect.left < other.rect.left):
            x_direction_sign = -1
        if(self.rect.top < other.rect.top):
            y_direction_sign = -1
        new_xvel = 2*x_direction_sign
        new_yvel = 2*y_direction_sign
        self.xvel = new_xvel
        self.yvel = new_yvel 
        self.bounce_count = 40

    def bounce(self):
        if(self.bounce_count <= 0): 
            return
        self.collide(self.xvel,self.yvel)
        self.updatePosition()
        self.bounce_count -= 1

    def immobilize(self,duration):
        self.mobile = False
        pygame.time.set_timer(USEREVENT + 1, duration) #THIS IS A TEMP FIX

    def mobilize(self):
        self.mobile = True