""" The only being directly controlled by the person playing the game.
"""

from being import *
from lantern import *
from exitblock import *
from platform import *
from weaponfactory import build_weapon, SWORD

#from sword import * #TEMP

class Player(Being):
    """ Player( AnimationSet, Level ) -> Player

    The player's inheritance from Being handles most, but not all of the physics that apply to it.
    A lot of mechanics like inventory and health have not been implemented for the player yet.

    Attributes:

    active: This flags whether the player is affected by gravity and keyboard input.

    can_jump: This flags whether pressing space will make the player jump.

    left, right, down, up, space, control, x: these represent keyboard inputs that make the player move.

    movement_state: a string key used to map the player's current conditions to the proper physics that should affect him.

    lantern: Currently represents the player's lantern, if he has one. This may be wrapped in inventory later on.
    """
    def __init__(self, player_animations, start_level):
        Being.__init__(self, player_animations)
        self.changeAnimation('idle','right')
        self.direction_id = 'right'
        self.animated = True
        self.default_image = self.animation.images[0]
        self.current_level = start_level
        self.can_leave_level = True
        self.active = True
        self.can_jump = True
        self.left, self.right, self.down, self.up, self.space, self.control, self.x = False, False, False, False, False, False, False
        self.movement_state = DEFAULT_MOVEMENT_STATE
        self.lantern = None

        #TODO: come up with a more general system for swords/weapons
        self.viewed_cutscene_keys = []
        #TEMP
        self.sword = build_weapon(SWORD, self)
        self.hit_points = [10, 10]
        #TEMP

    def temp_z_method(self):    
        #TEMP (no docstring)
        #TODO: find some way to pass this directional check into the sword itself.
        self.sword.activate(32, 0, self.direction_id) 
        #TODO: make a sword-swinging animation for the player, and set it so that the player cannot face the other way if moving left while swinging right (i.e., he just walks backwards)
        #TEMP

    @staticmethod
    def load_player_animation_set():
        """ load_player_animation_set( ) -> AnimationSet

        Load all animations that the player can use and put them into an AnimationSet object.
        """
        player_rect = Rect(0, 0, 32, 64)
        filepath = './LevelEditor/animations/player/'
        
        # could probably use the same system used for loading monster animations, and simply store
        # player animation keys in tiledata with the other keys.
        
        # NOTE: change/add player sprites here.
        
        player_idle_left = GameImage.load_animation(filepath, 'player_1_idle_left.bmp', player_rect, -1)
        player_idle_right = GameImage.load_animation(filepath, 'player_1_idle_right.bmp', player_rect, -1)

        player_walking_left = GameImage.load_animation(filepath, 'player_1_walking_left.bmp', player_rect, -1, True, 6)
        player_walking_right = GameImage.load_animation(filepath, 'player_1_walking_right.bmp', player_rect, -1, True, 6)

        player_running_left = GameImage.load_animation(filepath, 'player_1_walking_left.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_running_left.bmp', player_rect, -1, True, 5)
        player_running_right = GameImage.load_animation(filepath, 'player_1_walking_right.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_running_right.bmp', player_rect, -1, True, 5)

        player_jumping_left = GameImage.load_animation(filepath, 'player_1_idle_left.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_jumping_left.bmp', player_rect, -1, True, 12)
        player_jumping_right = GameImage.load_animation(filepath, 'player_1_idle_right.bmp', player_rect, -1) # TODO: GameImage.load_animation(filepath, 'player_1_jumping_right.bmp', player_rect, -1, True, 12)

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
        """ p.deactivate( ) -> None

        Make the player unable to move, as for a cutscene.
        """
        self.active = False
        self.up, self.down, self.left, self.right, self.space, self.control, self.x = False, False, False, False, False, False, False

    def activate(self):
        """ p.activate( ) -> None

        >setters in python
        >2014
        """
        self.active = True

    def update(self, tiles, light_map):
        """ p.update( [ [ Tile ] ], [ [ double ] ]) -> None

        Exit the level if the player is outside its boundaries.
        Otherwise, figure out the current movement state and apply physics accordingly.
        All entities that "care" about the player (monsters, NPCs, etc.) then act.
        Afterwards, update the player's view (indirectly updating the screen).
        """
        if(self.exitLevelCheck()): return
        update_method = MOVEMENT_STATE_MAP[self.movement_state]
        update_method(self)
        self.invincibility_update()
        self.lantern_update()
        Being.updatePosition(self)
        player_interactables = self.current_level.player_interactables()
        for e in player_interactables:
            e.update(self)
        self.updateView(tiles, light_map)


    def default_move_update(self):  #consider separating midair update into its own method if this gets too complex.
        """ p.default_move_update( ) -> None

        Check which buttons are currently being pressed and move the player accordingly.
        This is a little complicated, so I can go more in-depth if necessary.
        """
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
        """ p.bounce_move_update( ) -> None

        Calls the player's bounce method. This is generally done if the player has just been knocked back by an enemy.
        """
        self.bounce()

    def ladder_move_update(self):
        """ p.ladder_move_update( ) -> None

        This update is called if the player is grabbing onto a ladder. Note that this doesn't happen if the player is in collision with the ladder,
        only if he actually "grabs" it by pressing up.
        """
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

    def invincibility_update(self):
        """ p.invincibility_update( ) -> None

        Advances the player's invincibility frames.
        """
        if self.invincibility_frames > 0: self.invincibility_frames -= 1

    def lantern_update(self):
        """ p.lantern_update( ) -> None

        Update the player's lantern (draining oil) if the player is underground and holding a lantern.
        """
        if self.lantern and self.active and not self.current_level.outdoors:
            self.lantern.oil_update()

    def x_action_check(self):
        """ p.x_action_check( ) -> None

        If the player presses x, the first thing he is found to be in range of is activated.
        This includes doors, signs, and NPCs.
        """
        x_interactables = self.current_level.x_interactable_objects()
        for x in x_interactables:
            if x.in_interact_range(self) or pygame.sprite.collide_rect(self, x):
                self.x_interact(x)
                return

    def x_interact(self, interactable):
        """ p.x_interact( ? ) -> None

        This is an extension of x_action_check.
        """
        interactable.execute_x_action(self.current_level, self)
     
     #this gets laggy when there is too much light. try to fix it. (might have to fix other methods instead)
    def updateView(self, all_tiles, light_map): #note: this is only to be used in "cave" settings. for areas that are outdoors, use something else.
        """ p.updateView( [ [ Tile ] ], [ [ double ] ]) -> None

        Use the given light map of the level to figure out how bright each tile should be (assuming the player is underground).
        This updates the player's view and makes visible light sources emit light.
        """
        level = self.current_level
        lanterns = level.getLanterns()

        coords = self.coordinates()
        start_x = max(0, coords[0] - self.sight_dist() - 2)
        end_x = min(len(all_tiles[0]), coords[0] + self.sight_dist() + 2)
        start_y = max(0, coords[1] - self.sight_dist() - 2)
        end_y = min(len(all_tiles), coords[1] + self.sight_dist() + 2)

        GameImage.updateAnimation(self, 256)         
        if(self.current_level.outdoors):
            return
        nearby_light_sources = []
        far_light_sources = []
        for l in lanterns:
            l.update(self)
            if self.in_vision_range(l):
                nearby_light_sources.append(l)
            else:
                far_light_sources.append(l)
        for f in far_light_sources:
       	    f.update_light(all_tiles, light_map)
        self.emit_light(self.sight_dist(), all_tiles, light_map, nearby_light_sources)

    def sight_dist(self):
        """ p.sight_dist( ) -> int 

        Returns the radius of light that the player's lantern should emit.
        """
        if self.lantern and not self.lantern.is_empty():
            return self.lantern.light_distance()
        return 0 

    def in_vision_range(self, other):	
        """ p.in_vision_range( ? ) -> bool 

        Checks if the player can see the given object in the dark.
        """
        if(self.withindist(other, self.sight_dist() + other.light_distance())):
            return True
        else:
            return False 

            #this could probably be moved up in inheritance
    def get_point(self, start, end, slope, x):
        # this seems to be unused, but I don't want to get rid of it unless I'm sure.
        p = start
        if(start[0] > end[0]): 
            p = end
        y = p[1] + slope*(x - p[0])
        return (x, y)

    #TODO: collidewith could be an abstract method in the object we collide with
    #TODO: could speed this method up by only checking collidable objects near the player.

    def take_damage(self, damage):
        """ p.take_damage( int ) -> None
        
        The player receives the given amount of damage.
        Since the game would be a pain to test if the player could die, this is not yet implemented.
        """
        if damage <= 0: return
        self.hit_points[0] -= damage


    def collide(self, xvel, yvel):
        """ p.collide( int, int ) -> None

        The player collides with any adjacent objects that he is in contact with.
        This includes stopping against platforms, being hit by monsters, absorb pickups, etc.
        """
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

    def collide_ladder(self): #
        """ p.collide_ladder( ) -> bool

        Note that this is a boolean, not an action. (might be a more general and efficient way to implement the check for what object(s) the player is currently colliding with.)
        This is called if the player presses up, and checks to see whether the player grabs onto a ladder.
        """
        ladders = self.current_level.getLadders()
        for l in ladders:
            if pygame.sprite.collide_rect(self, l):
                return True
        return False

    def collideExits(self):
        """ p.collideExits( ) -> None

        Check if the player should leave the level.
        The way this method is written sort of confuses me, because the exit blocks are supposed to stop the player from leaving the level.
        """
        exits = self.current_level.get_exit_blocks()
        for e in exits:
            if pygame.sprite.collide_rect(self, e):
                self.exitLevel(e)
                return

    def collidePickups(self):
        """ p.collidePickups( ) -> None

        The player absorbs any pickups he is in contact with.
        """
        level = self.current_level
        pickups = level.getPickups()
        for p in pickups:
            if pygame.sprite.collide_rect(self, p):
                self.pick_up(p)
                return

    def collideLanterns(self):
        """ p.collideLanterns( ) -> None

        The player picks up any lanterns he is touching.
        This may change if the player instead gets lanterns from a chest, has to press a button to pick them up, etc.
        """
        level = self.current_level
        lanterns = level.getLanterns()
        for l in lanterns:
            if pygame.sprite.collide_rect(self, l):
                self.pick_up_lantern(l) #TEMP
                return

    def pick_up(self, pickup):
        """ p.pick_up( Pickup ) -> None

        The player absorbs a pickup, removing it from the level.
        """
        pickup.delete()
        pickup.take_effect(self)

        #TEMP METHOD (therefore no docstring)
    def pick_up_lantern(self, lantern):
        lantern.delete()
        self.lantern = lantern
        #TEMP METHOD

    def collideMonsters(self, xvel, yvel):
        """ p.collideMonsters( int, int ) -> None

        If the player is touching any monsters, he gets hurt and bounces off of them.
        """
        if self.invincibility_frames > 0: return
        x_direction_sign = 1
        y_direction_sign = 1
        level = self.current_level
        monsters = level.getMonsters()
        for m in monsters:
            if pygame.sprite.collide_rect(self, m):
                self.mask = pygame.mask.from_surface(self.image)
                m.mask = pygame.mask.from_surface(m.image)
                if pygame.sprite.collide_mask(self, m):
                    self.collide_with_damage_source(m)
                    break #makes sure the player can only collide with one monster per cycle

    def collide_with_damage_source(self, source):
        """ p.collide_with_monster( Monster/Weapon ) -> None

        A player being hit by a monster, weapon, projectile, etc. takes damage, goes through invincibility frames, etc.
        """
        self.bounceAgainst(source)
        self.invincibility_frames = 60
        source.bounceAgainst(self)
        

    def bounce(self):
        """ p.bounce( ) -> None

        The player performs one frame of being bounced away from an enemy.
        """
        if(self.bounce_count <= 0): 
            self.movement_state = DEFAULT_MOVEMENT_STATE
            return
        self.bounce_count -= 1

    def bounceAgainst(self, other): 
        """ b.bounceAgainst ( Being ) -> None

        Bounce against another being, starting the bounce counter so that the player cannot
        take other actions until the counter runs out.
        Similar to Being's bounceAgainst, except it alters the current state.
        """
        if self.invincibility_frames > 0: return
        x_direction_sign = 1
        y_direction_sign = 1
        if(self.rect.left < other.rect.left):
            x_direction_sign = -1
        if(self.rect.top < other.rect.top):
            y_direction_sign = -1
        new_xvel = 4 * x_direction_sign
        new_yvel = y_direction_sign
        self.xvel = new_xvel
        self.yvel = new_yvel 
        self.movement_state = BOUNCING_MOVEMENT_STATE
        self.bounce_count = 15

    def light_distance(self):
        """ p.light_distance( ) -> int

        Returns the radius of light emitted by the player in darkness.
        """
    	return self.sight_dist()

    def exitLevelCheck(self):
        """ p.exitLevelCheck() -> bool

        Checks whether the player is outside the level and send him to the adjacent level in that direction if necessary.
        """
        if(self.current_tile() == None):
            #a bug can sometimes occur here, crashing the game. (this is rare however.)
            self.exitLevel(self.coordinates())
            return True
        return False

    def exitLevel(self, coords):
        """ p.exitLevel( ( int, int ) ) -> None 

        Move the player to the proper adjacent level.
        This is called if the player is outside the current level.
        """
        self.current_level.movePlayer(coords)

    def pause_game(self):
        """ p.pause_game( ) -> None

        Pause the game and open the pause screen (which is currently the map screen).
        """
        self.current_level.pause_game(self)

    def unpause_game(self):
        """ p.unpause_game( ) -> None

        Resume normal gameplay.
        """
        self.current_level.unpause_game(self)

    def has_viewed_cutscene(self, cutscene_key):
        """ p.has_viewed_cutscene( str ) -> bool

        Check whether the player has seen a cutscene based on its associated string key.
        """
        return cutscene_key in self.viewed_cutscene_keys

    def get_lantern(self):
        """ p.get_lantern( ) -> Lantern

        AHAHAHAHAHAHAHAHA oh wait you're serious
        """
        return self.lantern

    def hittable_targets(self):
        """ p.hittable_targets( ) -> [ Monster ]

        Returns everything that can be hit by the player's weapons. Currently only includes monsters.
        """
        return self.current_level.getMonsters()

DEFAULT_MOVEMENT_STATE = "default_movement_state"
BOUNCING_MOVEMENT_STATE = "bouncing_movement_state"
LADDER_MOVEMENT_STATE = "ladder_movement_state"

MOVEMENT_STATE_MAP = {
    DEFAULT_MOVEMENT_STATE:Player.default_move_update,
    BOUNCING_MOVEMENT_STATE:Player.bounce_move_update,
    LADDER_MOVEMENT_STATE:Player.ladder_move_update
}