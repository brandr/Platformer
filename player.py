from being import *
from lantern import *
from exitblock import *
from platform import *

from sword import * #TEMP

class Player(Being):
    def __init__(self, player_animations, start_level):
        Being.__init__(self, player_animations)
        self.changeAnimation('idle','right')
        self.direction_id = 'right'
        self.animated = True
        self.default_image = self.animation.images[0]
        self.current_level = start_level

        self.active = True
        self.can_jump = True
        self.left, self.right, self.down, self.up, self.space, self.control, self.x = False, False, False, False, False, False, False
        self.movement_state = DEFAULT_MOVEMENT_STATE

        self.lantern = None

        #TODO: come up with a more general system for swords/weapons
        self.sword = Sword(self)
        #TEMP

    def temp_z_method(self):    
        #TEMP
        #TODO: find some way to pass this directional check into the sword itself.
        self.sword.activate(32, 0, self.direction_id) 
        #TODO: make a sword-swinging animation for the player, and set it so that the player cannot face the other way if moving left while swinging right (i.e., he just walks backwards)
        #TEMP

    @staticmethod
    def load_player_animation_set():
        player_rect = Rect(0, 0, 32, 64)
        filepath = './LevelEditor/animations/player/'
        
        # could probably use the same system used for loading monster animations, and simply store
        # player animation keys in tiledata with the other keys.
        
        # NOTE: change/add player sprites here.
        
        player_idle_left = GameImage.load_animation(filepath, 'player_1_idle_left.bmp', player_rect, -1)
        player_idle_right = GameImage.load_animation(filepath, 'player_1_idle_right.bmp', player_rect, -1)

        player_walking_left = GameImage.load_animation(filepath, 'player_1_walking_left.bmp', player_rect, -1, True, 6)
        player_walking_right = GameImage.load_animation(filepath, 'player_1_walking_right.bmp', player_rect, -1, True, 6)

        player_running_left = GameImage.load_animation(filepath, 'player_running_left.bmp', player_rect, -1, True, 5)
        player_running_right = GameImage.load_animation(filepath, 'player_running_right.bmp', player_rect, -1, True, 5)

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
        self.active = False
        self.up, self.down, self.left, self.right, self.space, self.control, self.x = False, False, False, False, False, False, False

    def activate(self):
        self.active = True

    def update(self, tiles, light_map):
        if(self.exitLevelCheck()): return
        update_method = MOVEMENT_STATE_MAP[self.movement_state]
        update_method(self)
        self.lantern_update()
        Being.updatePosition(self)
        self.updateView(tiles, light_map)

    def default_move_update(self):#, tiles, light_map = None):   #consider separating midair update into its own method if this gets too complex.
        up, down, left, right, space, running, x = self.up, self.down, self.left, self.right, self.space, self.control, self.x
        self.xvel = 0
        if x:
            if self.x_action_check(): return
        if up:
            if self.collide_ladder():
                self.movement_state = LADDER_MOVEMENT_STATE

        if down:
            pass

        if left and not right:
            self.xvel = -3
            self.direction_id = 'left'

        if right and not left:
            self.xvel = 3
            self.direction_id = 'right'

        if space and self.onGround:
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

    def bounce_move_update(self):
        self.bounce()

    def ladder_move_update(self):
        #TODO: ladder climbing animations go here
        up, down, left, right, space, running, x = self.up, self.down, self.left, self.right, self.space, self.control, self.x
        self.xvel, self.yvel = 0, 0
        if not self.collide_ladder():
            self.movement_state = DEFAULT_MOVEMENT_STATE
            return
        #TODO: make behavior at the top and bottom of a ladder less awkward.
        if up and not down:         
            self.yvel = -2      

        elif down and not up: 
            self.yvel = 2

        if left and not right:
            self.xvel = -2
            self.direction_id = 'left'

        if right and not left:
            self.xvel = 2
            self.direction_id = 'right'

    def lantern_update(self):
        if self.lantern and self.active and not self.current_level.outdoors:
            self.lantern.oil_update()

    def x_action_check(self):
        x_interactables = self.current_level.x_interactable_objects()
        for x in x_interactables:
            if x.in_interact_range(self) or pygame.sprite.collide_rect(self, x):
                self.x_interact(x)
                return

    def x_interact(self, interactable):
        interactable.execute_x_action(self.current_level, self)
     
     #this gets laggy when there is too much light. try to fix it. (might have to fix other methods instead)
    def updateView(self, all_tiles, light_map): #note: this is only to be used in "cave" settings. for areas that are outdoors, use something else.
        level = self.current_level
        player_interactables = level.player_interactables()
        lanterns = level.getLanterns()

        coords = self.coordinates()
        start_x = max(0, coords[0] - self.sight_dist() - 2)
        end_x = min(len(all_tiles[0]), coords[0] + self.sight_dist() + 2)
        start_y = max(0, coords[1] - self.sight_dist() - 2)
        end_y = min(len(all_tiles), coords[1] + self.sight_dist() + 2)

        GameImage.updateAnimation(self, 256) 
        for e in player_interactables:      #TODO: move this and other parts to a different method, since they have nothing to do with view.
            e.update(self)
        if(self.current_level.outdoors):
            return
        nearby_light_sources = []
        far_light_sources = []
        for l in lanterns:
            l.update(self)
            if self.invisionrange(l):
                nearby_light_sources.append(l)
            else:
                far_light_sources.append(l)
        for f in far_light_sources:
       	    f.update_light(all_tiles, light_map)
        self.emit_light(self.sight_dist(), all_tiles, light_map, nearby_light_sources)

    def sight_dist(self):
        if self.lantern and not self.lantern.is_empty():
            return self.lantern.light_distance()
        return 0 #TODO: get sight_dist from self.lantern

    def invisionrange(self, other):	#checks if the player can see a platform
        if(self.withindist(other, self.sight_dist() + other.light_distance())):
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

    #TODO: collidewith could be an abstract method in the object we collide with
    #TODO: could speed this method up by only collecting collidable objects near the player.
    def collide(self, xvel, yvel):
        level = self.current_level
        platforms = level.get_impassables() #TODO: remember that it might be possible to pass through some platforms in some directions.
        slopes = []
        default_platforms = []
        for p in platforms:
            if pygame.sprite.collide_mask(self, p) and p.is_solid:
                if p.is_sloped:
                    slopes.append(p)
                else:
                    default_platforms.append(p)
        for s in slopes:
            Being.collideWith(self, xvel, yvel, s)
        for p in default_platforms:
            Being.collideWith(self, xvel, yvel, p)
        self.collideExits()
        self.collidePickups()
        self.collideLanterns() #might not need this with the new lantern system (if lantern is obtained  from a chest or something)
        if(self.bounce_count <= 0):
            self.collideMonsters(xvel, yvel)

    def collide_ladder(self): #note that this is a boolean, not an action. (might be a more general and efficient way to implement the check for what object(s) the player is currently colliding with)
        ladders = self.current_level.getLadders()
        for l in ladders:
            if pygame.sprite.collide_rect(self, l):
                return True
        return False

    def collideExits(self):
        exits = self.current_level.get_exit_blocks()
        for e in exits:
            if pygame.sprite.collide_rect(self, e):
                self.exitLevel(e)
                return

    def collidePickups(self):
        level = self.current_level
        pickups = level.getPickups()
        for p in pickups:
            if pygame.sprite.collide_rect(self, p):
                self.pick_up(p)
                return

    def collideLanterns(self):
        level = self.current_level
        lanterns = level.getLanterns()
        for l in lanterns:
            if pygame.sprite.collide_rect(self, l):
                self.pick_up_lantern(l) #TEMP
                return

    def pick_up(self, pickup):
        pickup.delete()
        pickup.take_effect(self)

        #TEMP METHOD
    def pick_up_lantern(self, lantern):
        lantern.delete()
        self.lantern = lantern
        #TEMP METHOD

    def collideMonsters(self, xvel, yvel):
        x_direction_sign = 1
        y_direction_sign = 1
        level = self.current_level
        monsters = level.getMonsters()
        for m in monsters:
            if pygame.sprite.collide_rect(self, m):
                self.mask = pygame.mask.from_surface(self.image)
                m.mask = pygame.mask.from_surface(m.image)
                if pygame.sprite.collide_mask(self, m):
                    if(self.rect.left < m.rect.left):
                        x_direction_sign = -1
                    if(self.rect.top < m.rect.top):
                        y_direction_sign = -1
                    new_xvel = 4*x_direction_sign
                    new_yvel = y_direction_sign
                    self.xvel = new_xvel
                    self.yvel = new_yvel 
                    self.movement_state = BOUNCING_MOVEMENT_STATE
                    self.bounce_count = 15
                    m.bounceAgainst(self)
                    break #makes sure the player can only collide with one monster per cycle

    def bounce(self):
        if(self.bounce_count <= 0): 
            self.movement_state = DEFAULT_MOVEMENT_STATE
            return
        self.bounce_count -= 1

    def light_distance(self):
    	return self.sight_dist()

    def exitLevelCheck(self):
        if(self.current_tile() == None):
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

    def get_lantern(self):
        return self.lantern

DEFAULT_MOVEMENT_STATE = "default_movement_state"
BOUNCING_MOVEMENT_STATE = "bouncing_movement_state"
LADDER_MOVEMENT_STATE = "ladder_movement_state"

MOVEMENT_STATE_MAP = {
    DEFAULT_MOVEMENT_STATE:Player.default_move_update,
    BOUNCING_MOVEMENT_STATE:Player.bounce_move_update,
    LADDER_MOVEMENT_STATE:Player.ladder_move_update
}