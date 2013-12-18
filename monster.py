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
        self.max_speed = 4

#TODO: make this general in the long run, so that monsters can interact with each other as well as with the player.
    def update(self,player):
        self.updateAnimation()
        #TODO: check if the monster can see the player. (using sightdist)
        #TODO: check if the monster is hostile the player.
        self.batUpdate(player) #TEMPORARY

    def batUpdate(self,player):
        self.moveTowards(player.currenttile())
        Being.updatePosition(self)

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

