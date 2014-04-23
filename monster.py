import being
from being import *

# A monster is more specific than a being in that it moves around and has AI.
# However, it is not necessarily hostile to the player.
# It may have some commonalities with player. these should be moved up to Being where appropriate.
# It may even make sense to make player inherit from monster. Not sure yet, though.

class Monster(Being):
    def __init__(self, animations, x, y):#name, x, y): 
        Being.__init__(self,animations)
        # self.name = name	#not yet sure how useful a monster name will be. It seems reasonable enough though.
        self.name = None
        self.animated = True
        self.rect.centerx += x
        self.rect.centery += y
        self.sightdist = 6
        self.max_speed = 6
        self.direction_val = -1 # -1 for left, 1 for right
        self.direction_id = 'left'
        self.changeAnimation('idle','left')
        self.wait_count = 20 #TEMP. As monster behavior gets more complex, find other ways to set timers.

    #TODO: make this general in the long run, so that monsters can interact with each other as well as with the player.
        #  in particular, consider having monsters "collide" with each other (they probably shouldn't bounce but I'm not sure.)
    def update(self, player):
        self.updateAnimation()
        #TODO: check if the monster can see the player. (using sightdist)
        #TODO: check if the monster is hostile the player.
        #TODO: figure out a better way to assosciate the monster with its udpate action (probably a dict.)
        if self.name == "bat": #TEMPORARY
            self.batUpdate(player)
        elif self.name == "giant_frog": #TEMPORARY
            self.frogUpdate(player)
        Being.updatePosition(self)
        #TODO: giant frog animations and AI

    def batUpdate(self,player):
        target = player.currenttile()
        if(target != None):
            self.moveTowards(player.currenttile())

    def frogUpdate(self,player):
        self.gravityUpdate()
        self.faceTowards(player.currenttile())
        if self.onGround:
            self.changeAnimation('idle', self.direction_id)
            self.xvel = 0
            #TODO: make the frog try to land on the player.
                # figure out the frog's distance from the player, and calculate the necessary xvel.
                # jump with min(self.max_speed/2, target_speed)
            if self.wait_count <= 0:
                self.jump(self.direction_val*self.max_speed/2,self.max_speed)
            self.wait()

    def wait(self):
        if(self.wait_count <= 0): return
        self.wait_count -= 1

        #the jump method could go in Being as well.
    def jump(self,xvel = 0, yvel = 0): #TODO: figure out how a monster's jumping ability is determined.
        self.xvel += xvel
        self.yvel -= yvel
        #self.changeAnimation('jumping',self.direction_id)     #TODO
        self.animation.iter()
        self.wait_count = 25 #TEMP
        self.onGround = False

    def faceTowards(self, target):
        if(target != None):
            x_dist = target.coordinates()[0] - self.currenttile().coordinates()[0]
            if x_dist == 0: return
            self.direction_val = x_dist/abs(x_dist)
            #TEMP
            if self.direction_val == -1:
                self.direction_id = 'left'
            if self.direction_val == 1:
                self.direction_id = 'right'

    def gravityUpdate(self):    #NOTE: could probably make this a lot more general. (i.e., different terminal velocites for some monsters)
         if not self.onGround:    # only accelerate with gravity if in the air
            self.yvel += 0.3
            if self.yvel > 100: self.yvel = 100

    def updateAnimation(self, light_value = None):
        Being.updateAnimation(self,light_value)
