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
        Being.__init__(self,player_animations)
        self.changeAnimation('idle','right')
        self.direction_id = 'right'
        self.animated = True
        self.default_image = self.animation.images[0]
        self.current_level = start_level
        self.sightdist = 2
        
    @staticmethod
    def load_player_animation_set():
        player_rect = Rect(0,0,32,64)
        filepath = './LevelEditor/animations/player/'
        
        # could probably use the same system used for loading monster animations, and simply store
            # player animation keys in tiledata with the other keys.
        
        player_idle_left = GameImage.load_animation(filepath, 'player_idle_left.bmp', player_rect, -1)
        player_idle_right = GameImage.load_animation(filepath, 'player_idle_right.bmp', player_rect, -1)

        player_walking_left = GameImage.load_animation(filepath, 'player_walking_left.bmp', player_rect, -1)
        player_walking_right = GameImage.load_animation(filepath, 'player_walking_right.bmp', player_rect, -1)

        player_running_left = GameImage.load_animation(filepath, 'player_running_left.bmp', player_rect, -1,True, 5)
        player_running_right = GameImage.load_animation(filepath, 'player_running_right.bmp', player_rect, -1,True, 5)

        player_jumping_left = GameImage.load_animation(filepath, 'player_jumping_left.bmp', player_rect, -1, True, 12)
        player_jumping_right = GameImage.load_animation(filepath, 'player_jumping_right.bmp', player_rect, -1, True, 12)

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
        #TODO: move some or all of this stuff to "being", and break it up to be more extensible.
            #could also make a Movement class, held as a data type by player or being.
        if(self.exitLevelCheck()): return
        if(self.bounce_count > 0):
            self.bounce()
            return
        self.xvel = 0
        if down:
            pass
        if left and not right:
            self.xvel = -4
            self.direction_id = 'left'
        if right and not left:
            self.xvel = 4
            self.direction_id = 'right'
        if up:            # only jump if on the ground
            if self.onGround:  
                self.yvel -= 9
                self.changeAnimation('jumping',self.direction_id)
                self.animation.iter()
                self.onGround = False
        if not self.onGround:    # only accelerate with gravity if in the air
            self.yvel += 0.3
            #TODO: falling animation starts once self.yvel >=0 (or maybe slightly lower/higher)
            # max falling speed
            if self.yvel > 100: self.yvel = 100
            #TODO: consider a separate falling animation at terminal velocity.
        else:
            self.running = running
        if(self.running):
            self.xvel *= 1.6
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

        Being.updatePosition(self)
        self.updateView()
     
     #this gets laggy when there is too much light. try to fix it. (might have to fix other methods instead)
    def updateView(self): #note: this is only to be used in "cave" settings. for areas that are outdoors, use something else.
        level = self.current_level
        tiles = level.getTiles()
        entities = level.getEntities()
        lanterns = level.getLanterns()
        
        GameImage.updateAnimation(self,256) 
        for e in entities:
            if(e != self):
               e.update(self)
        if(self.current_level.outdoors):
            return
        for row in tiles:    #IDEA: if the program becomes very slow, could limit tiles/lanterns to only the ones on camera. 
            for t in row:    #(might need to add 1 to each border though)
                if t.mapped:
                    t.updateimage()
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

    def invisionrange(self, other):	#checks if the player can see a platform
        if(self.withindist(other, self.sightdist+other.light_distance())):
            return True
        else:
            return False 

            #this could probably be moved up in inheritance
    def getpoint(self,start,end,slope,x):
        p = start
        if(start[0] > end[0]): 
            p = end
        y = p[1] + slope*(x-p[0])
        return (x, y)

            #this could probably be moved up in inheritance
    def insiderect(self,p,c1,c2):
        xrectcheck = p[0] >= c1[0] and p[0] <= c2[0] 
        yrectcheck = p[1] >= c1[1] and p[1] <= c2[1] 
        return xrectcheck and yrectcheck

        #only difference between player and gameimage moverect is whether centerx/y or left/top are used
        #for position. This is not very extensible, so should try to move these methods up in inheritance without breaking the program
    def moveTo(self, coords):
        self.moveRect(coords[0]*32,coords[1]*32,True)

    def moveRect(self,x_offset,y_offset,absolute = False):
        if(absolute):
            self.rect.left = x_offset
            self.rect.top = y_offset
            return
        self.rect.left += x_offset
        self.rect.top += y_offset

#TODO: collide could be an abstract method in the object we collide with
    def collide(self, xvel, yvel):

        level = self.current_level
        platforms = level.getPlatforms()

        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                Being.collideWith(self, xvel,yvel,p)
        self.collideExits()
        self.collideLanterns()
        if(self.bounce_count <= 0):
            self.collideMonsters(xvel,yvel)

    def collideExits(self):
        exits = self.current_level.get_exit_blocks()
        for e in exits:
            if pygame.sprite.collide_rect(self, e):
                self.exitLevel(e)
                return
                #TODO: figure out how to handle exitblocks with new system

    def collideLanterns(self):
        level = self.current_level
        lanterns = level.getLanterns()
        for l in lanterns:
            if pygame.sprite.collide_rect(self, l):
                l.delete()
                self.sightdist += l.lightvalue

    def collideMonsters(self,xvel,yvel):
        x_direction_sign = 1
        y_direction_sign = 1
        level = self.current_level
        monsters = level.getMonsters()
        for m in monsters:
            if pygame.sprite.collide_rect(self, m):
                if(self.rect.left < m.rect.left):
                    x_direction_sign = -1
                if(self.rect.top < m.rect.top):
                    y_direction_sign = -1
                new_xvel = 4*x_direction_sign
                new_yvel = y_direction_sign
                self.xvel = new_xvel
                self.yvel = new_yvel 
                self.bounce_count = 15
                m.bounceAgainst(self)
                break #makes sure the player can only collide with one monster per cycle

    def bounce(self):
        if(self.bounce_count <= 0): return
        self.collide(self.xvel,self.yvel)
        self.updatePosition()
        self.updateView()
        self.bounce_count -= 1

    def light_distance(self):
    	return self.sightdist

    def exitLevelCheck(self):
        if(self.currenttile() == None):
            #a bug can sometimes occur here.
            self.exitLevel(self.coordinates())
            return True
        return False

    def exitLevel(self, coords):
        self.current_level.movePlayer(coords)