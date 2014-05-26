from being import *
from lantern import *
from exitblock import *
from platform import *

class Player(Being):
    def __init__(self, player_animations, start_level):
        Being.__init__(self, player_animations)
        self.changeAnimation('idle','right')
        self.direction_id = 'right'
        self.animated = True
        self.default_image = self.animation.images[0]
        self.current_level = start_level
        self.sightdist = 2 #TEMP. I usually use 2 though.
        self.can_jump = True
        self.on_ladder = False #TEMP
        self.left, self.right, self.down, self.up, self.space, self.control = False, False, False, False, False, False
        
    @staticmethod
    def load_player_animation_set():
        player_rect = Rect(0, 0, 32, 64)
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
        animation_set.insertAnimation(player_idle_left,'left', 'idle')
        animation_set.insertAnimation(player_idle_right,'right', 'idle')

        animation_set.insertAnimation(player_walking_left,'left', 'walking')
        animation_set.insertAnimation(player_walking_right,'right','walking') 

        animation_set.insertAnimation(player_running_left,'left', 'running')
        animation_set.insertAnimation(player_running_right,'right', 'running')

        animation_set.insertAnimation(player_jumping_left,'left', 'jumping')
        animation_set.insertAnimation(player_jumping_right,'right', 'jumping')

        #TODO: jumping, falling, and (maybe) terminal velocity
        #TODO: attacking, other sprite animations

        return animation_set

    def deactivate(self):
        self.up, self.down, self.left, self.right, self.space, self.control = False, False, False, False, False, False

    def update(self, tiles):
        #TODO: move some of this stuff to "being", and break it up to be more extensible.
            #could also make a Movement class, held as a data type by player or being.

        if(self.exitLevelCheck()): return
        if(self.bounce_count > 0):
            self.bounce()
        

        up, down, left, right, space, running = self.up, self.down, self.left, self.right, self.space, self.control

        if up and self.up_action_check():
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

        if self.on_ladder:  #TEMP
            self.onGround = True
            self.yvel = 0

        if up and not down:            # only jump if on the ground
            if self.on_ladder:         # TEMP. need more sophisticated checks as we implement more movement situations.
                self.yvel = -2
                #TODO: ladder climing animation goes here

        if down and not up: 
            if self.on_ladder: #TEMP
                self.yvel = 2

        if space and self.onGround and not self.on_ladder: 
                self.yvel -= 8.0
                self.changeAnimation('jumping', self.direction_id)
                self.animation.iter()
                self.onGround = False
                self.can_jump = True

        if not self.onGround:    # only accelerate with gravity if in the air
            self.yvel += 0.35
            #TODO: falling animation starts once self.yvel >=0 (or maybe slightly lower/higher)
            # max falling speed
            if self.yvel > 90: self.yvel = 90
            if not space or self.yvel > 0:
                self.yvel = max(self.yvel, 0)
                self.can_jump = False
            #TODO: consider a separate falling animation at terminal velocity.
        else:
            self.running = running
        if(self.running):
            self.xvel *= 1.6
            if(self.onGround):
                self.changeAnimation('running', self.direction_id)
        else:
            if(self.onGround):
                if(left != right):
                    self.changeAnimation('walking', self.direction_id)
                else:
                    self.xvel = 0
                    self.changeAnimation('idle', self.direction_id)
            else: 
                if(left == right):
                    self.xvel = 0

        Being.updatePosition(self)
        self.updateView(tiles)

    def up_action_check(self):
        ups = self.current_level.up_interactable_objects()
        for u in ups:
            if pygame.sprite.collide_rect(self, u):
                self.up_interact(u)

    def up_interact(self, interactable):
        interactable.execute_event(self.current_level)
     
     #this gets laggy when there is too much light. try to fix it. (might have to fix other methods instead)
    def updateView(self, all_tiles): #note: this is only to be used in "cave" settings. for areas that are outdoors, use something else.
        level = self.current_level
        #entities = level.getEntities()
        player_interactables = level.player_interactables()
        lanterns = level.getLanterns()

        coords = self.coordinates()
        start_x = max(0, coords[0] - self.sightdist - 2)
        end_x = min(len(all_tiles[0]), coords[0] + self.sightdist + 2)
        start_y = max(0, coords[1] - self.sightdist - 2)
        end_y = min(len(all_tiles), coords[1] + self.sightdist + 2)

        GameImage.updateAnimation(self, 256) 
        for e in player_interactables:
            e.update(self)
        if(self.current_level.outdoors):
            return
        nearby_light_sources = []
        far_light_sources = []
        for l in lanterns:
            if self.invisionrange(l):
                nearby_light_sources.append(l)
            else:
                far_light_sources.append(l)
        for row in all_tiles[start_y:end_y]:    #IDEA: if the program becomes very slow, could limit tiles/lanterns to only the ones on camera. 
            for t in row[start_x:end_x]:    #(might need to add 1 to each border though)
                if t.mapped:
                    t.updateimage()
        for f in far_light_sources:
        	f.update_light(all_tiles)
        self.emit_light(self.sightdist, all_tiles, nearby_light_sources)

    def invisionrange(self, other):	#checks if the player can see a platform
        if(self.withindist(other, self.sightdist + other.light_distance())):
            return True
        else:
            return False 

            #this could probably be moved up in inheritance
    def getpoint(self, start, end, slope, x):
        p = start
        if(start[0] > end[0]): 
            p = end
        y = p[1] + slope*(x - op[0])
        return (x, y)

#TODO: collide could be an abstract method in the object we collide with
    def collide(self, xvel, yvel):
        level = self.current_level
        platforms = level.getPlatforms() #TODO: remember that it might be possible to pass through some platforms in some directions.
        slopes = []
        default_platforms = []
        for p in platforms:
            if p.is_sloped:
                slopes.append(p)
            else:
                default_platforms.append(p)
        for s in slopes:
            if pygame.sprite.collide_mask(self, s):
                Being.collideWith(self, xvel, yvel, s)
        for p in platforms:
            if pygame.sprite.collide_mask(self, p):
                Being.collideWith(self, xvel, yvel, p)
        self.collideLadders() #TEMP
        self.collideExits()
        self.collideLanterns()
        if(self.bounce_count <= 0):
            self.collideMonsters(xvel, yvel)

    def collideLadders(self): #TEMP. if other blocks alter player motion (which they probably will), should handle this more generally.
        self.on_ladder = False  # could also consider having this check in the ladder class, not the player class (to keep player class shorter)
        ladders = self.current_level.getLadders()
        for l in ladders:
            if pygame.sprite.collide_rect(self, l):
                self.on_ladder = True

        #not sure if this method is still being used. If not, delete it.
    def collideExits(self):
        exits = self.current_level.get_exit_blocks()
        for e in exits:
            if pygame.sprite.collide_rect(self, e):
                self.exitLevel(e)
                return

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
            #a bug can sometimes occur here, crashing the game. (this is rare however.)
            self.exitLevel(self.coordinates())
            return True
        return False

    def exitLevel(self, coords):
        self.current_level.movePlayer(coords)

    def pause_game(self):
        self.current_level.pause_game(self)

    def unpause_game(self):
        self.current_level.unpause_game(self)