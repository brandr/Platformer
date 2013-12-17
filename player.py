import being
from being import *
import lantern
from lantern import *
import exitblock
from exitblock import *
import platform
from platform import *

class Player(Being):
    def __init__(self,player_animations,start_level):
        #not sure if I'm still using player sprites, could probably make the arg an animationset instead
        Being.__init__(self,player_animations)#,Rect(0,0,32,64),-1)
        #self.changeDirection('right') #could extend this to gameImage/Entity (or some other class between player and gameimage)
        #self.animation = self.direction_set["idle"]
        self.changeAnimation('idle','right')
        self.direction_id = 'right'

        self.animated = True
        self.default_image = self.animation.images[0]
  
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.running = False
        self.sightdist = 3
        self.current_level = start_level

    @staticmethod
    def load_player_animation_set():
        player_rect = Rect(0,0,32,64)
        #could probably store this data even more generally, and make a "load animation set" method that takes args like these.
        #could also set up some structor that allows left and right animations to be loaded from the same sheet
        player_idle_left = GameImage.load_animation('player_idle_left.bmp', player_rect, 2, -1)
        player_idle_right = GameImage.load_animation('player_idle_right.bmp', player_rect, 2, -1)

        player_walking_left = GameImage.load_animation('player_walking_left.bmp', player_rect, 6, -1)
        player_walking_right = GameImage.load_animation('player_walking_right.bmp', player_rect, 6, -1)

        player_running_left = GameImage.load_animation('player_running_left.bmp', player_rect, 6, -1,True, 5)
        player_running_right = GameImage.load_animation('player_running_right.bmp', player_rect, 6, -1,True, 5)

        player_jumping_left = GameImage.load_animation('player_jumping_left.bmp', player_rect, 6, -1, True, 12)
        player_jumping_right = GameImage.load_animation('player_jumping_right.bmp', player_rect, 6, -1, True, 12) #TODO: change to "right" once I make the sprite.

        animation_set = AnimationSet(player_idle_right)
        animation_set.insertAnimation(player_idle_left,'left','idle')
        animation_set.insertAnimation(player_idle_right,'right','idle')

        animation_set.insertAnimation(player_walking_left,'left','walking')
        animation_set.insertAnimation(player_walking_right,'right','walking') 

        animation_set.insertAnimation(player_running_left,'left','running')
        animation_set.insertAnimation(player_running_right,'right','running')

        animation_set.insertAnimation(player_jumping_left,'left','jumping')
        animation_set.insertAnimation(player_jumping_right,'right','jumping')

        #TODO: jumping, falling, and (maybe) terminal velocity

        return animation_set

    def update(self, up, down, left, right, running):
        #a lot of this could be moved to a supeclass
        self.xvel = 0
        if down:
            pass
        if left and not right:
            self.xvel = -4
            self.direction_id = 'left'
            #self.changeDirection('left')
        if right and not left:
            self.xvel = 4
            self.direction_id = 'right'
            #self.changeDirection('right')
        if up:
            # only jump if on the ground
            if self.onGround:  
                self.yvel -= 9
                self.changeAnimation('jumping',self.direction_id)
                self.animation.iter()
                self.onGround = False
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            #TODO: falling animation starts once self.yvel >=0 (or maybe slightly lower/higher)
            # max falling speed
            if self.yvel > 100: self.yvel = 100
            #TODO: consider a separate falling animation at terminal velocity.
        else:
            self.running = running
        if(self.running):
            self.xvel *= 1.67
            if(self.onGround):
                self.changeAnimation('running',self.direction_id)
        else:
            if(self.onGround):
                if(left != right):
                    self.changeAnimation('walking',self.direction_id)
                else:
                    self.xvel = 0
                    self.changeAnimation('idle',self.direction_id)
            else: 
                if(left == right):
                    self.xvel = 0
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
        self.updateView()
        
    def updateView(self): #note: this is only to be used in "cave" settings. for areas that are outdoors, use something else.
        level = self.current_level
        tiles = level.getTiles()
        lanterns = level.getLanterns()
        
        GameImage.updateimage(self,256) 
        if(self.current_level.outdoors):return
        for row in tiles:    #IDEA: if the program becomes very slow, could limit tiles/lanterns to only the ones on camera. 
            for t in row:    #(might need to add 1 to each border though)
                if t.mapped:
                    t.updateimage(False)
        nearby_light_sources = []
        far_light_sources = []
        for l in lanterns:
            if self.invisionrange(l):
                nearby_light_sources.append(l)
            else:
                far_light_sources.append(l)
        for f in far_light_sources:
        	f.update_light(tiles)

        self.emit_light(self.sightdist,tiles,nearby_light_sources)

    def moveTo(self, coords):
        self.rect.left = coords[0]*32
        self.rect.top = coords[1]*32

    def invisionrange(self, other):	#checks if the player can see a platform
        if(self.withindist(other, self.sightdist+other.light_distance())):
            return True
        else:
            return False 

    def getpoint(self,start,end,slope,x):
        p = start
        if(start[0] > end[0]): 
            p = end
        y = p[1] + slope*(x-p[0])
        return (x, y)

    def insiderect(self,p,c1,c2):
        xrectcheck = p[0] >= c1[0] and p[0] <= c2[0] 
        yrectcheck = p[1] >= c1[1] and p[1] <= c2[1] 
        return xrectcheck and yrectcheck

    def collide(self, xvel, yvel): 
        level = self.current_level
        tiles = level.getTiles()
        entities = level.getEntities()
        platforms = level.getPlatforms()
        lanterns = level.getLanterns()

        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Lantern): #TODO: break this off into its own method as the program grows
                    p.delete()
                    self.sightdist += p.lightvalue
                if isinstance(p, ExitBlock):
                    self.exitLevel(p)
                    return
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

    def light_distance(self):
    	return self.sightdist

    def exitLevel(self, exit_block):
        self.current_level.movePlayer(exit_block)