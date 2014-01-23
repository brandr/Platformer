import being
from being import *

#a monster is more specific than a being in that it moves around and has AI.
#however, it is not necessarily hostile to the player.
#it may have some commonalities with player. these should be moved up to Being where appropriate.
#it may even make sense to make player inherit from monster. Not sure yet, though.

class Monster(Being):
    def __init__(self,animations,name,x,y): 
        Being.__init__(self,animations)
        self.name = name	#not yet sure how useful a monster name will be. It seems reasonable enough though.
        self.animated = True
        self.rect.centerx += x
        self.rect.centery += y
        self.sightdist = 6
        self.max_speed = 6
        self.direction_val = -1 #-1 for left, 1 for right
        self.direction_id = 'left'
        self.changeAnimation('idle','left')

        self.wait_count = 20 #TEMP. As monster behavior gets more complex, find other ways to set timers.

        #if self.name == "giant frog": #TEMP
        #    self.animated = False

#TODO: make this general in the long run, so that monsters can interact with each other as well as with the player.
    def update(self,player):
        self.updateAnimation()
        #TODO: check if the monster can see the player. (using sightdist)
        #TODO: check if the monster is hostile the player.

        #TODO: figure out a better way to assosciate the monster with its udpate action.
        if self.name == "bat": #TEMPORARY
            self.batUpdate(player)
        elif self.name == "giant frog": #TEMPORARY
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
            self.changeAnimation('idle',self.direction_id)
            self.xvel = 0
            #TODO: make the frog try to land on the player.
                # figure out the frog's distance from the player, and calculate the necessary xvel.
                # jump with min(self.max_speed/2, target_speed)
            if self.wait_count <= 0:
                self.jump(self.direction_val*self.max_speed/2,self.max_speed)
            self.wait()
        #TODO: wait, then hop towards player.

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

    #TEMPORARY (should be waaaaay more extensible)
    @staticmethod
    def load_bat_animation_set():
        bat_rect = Rect(0,0,32,32)
        bat_idle = GameImage.load_animation('bat_idle.bmp', bat_rect, 2, -1)
        animation_set = AnimationSet(bat_idle)
        animation_set.insertAnimation(bat_idle,'left','idle')
        animation_set.insertAnimation(bat_idle,'right','idle')
        return animation_set

    @staticmethod
    def load_giant_frog_animation_set():
        giant_frog_rect = Rect(0,0,64,64) #TEMP
        giant_frog_idle_left = GameImage.load_animation('giant_frog_idle_left.bmp', giant_frog_rect, 2, -1)
        giant_frog_idle_right = GameImage.load_animation('giant_frog_idle_right.bmp', giant_frog_rect, 2, -1)
        animation_set = AnimationSet(giant_frog_idle_left)
        animation_set.insertAnimation(giant_frog_idle_left,'left','idle')
        animation_set.insertAnimation(giant_frog_idle_right,'right','idle')
        return animation_set

#ANIMATION_MAP = {}#could put this in entity.
