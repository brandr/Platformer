""" A (possbly hostile) creature that lives in the dungeon somewhere.
"""

from being import *

class Monster(Being):
    """ Monster( AnimationSet, int, int ) -> AnimationSet

    A monster is more specific than a being in that it moves around and has AI.
    However, it is not necessarily hostile to the playerself.
    It may have some commonalities with player. these should be moved up to Being where appropriate.
    It may even make sense to make player inherit from monster. Not sure yet, though.

    Attributes:

    name: An identifier that can be used as a key to grab the monster's data.

    active: Determines whether the monster is able to move around (besides animation).

    sightdist: How far away the monster can spot you from in darkness. As far as I can tell, this isn't
    used right now, and it might be better to use a system that makes more sense, like having the monster
    become alerted to the player upon being hit by light from the player.

    max_speed: the highest speed the monster is capabale of moving in any direction. The monster may move
    slower than this value, but never faster.

    direction_val: A value set to -1 (left) or 1 (right) for the direction the player is moving in.

    direction_id: A string value to represent the direction.

    wait_count: A temporary value used to set timers in between the monster's actions.

    hit_points: An [int, int] value represeting [current hp, max hp]. Current hp cannot exceed max hp,
    and the monster dies when its current hp reaches 0.
    """
    def __init__(self, animations, x, y): 
        Being.__init__(self, animations, x, y)
        self.name = None
        self.animated = True
        self.active = True
        self.sightdist = 6
        self.max_speed = 6
        self.direction_val = -1 # -1 for left, 1 for right
        self.direction_id = 'left'
        self.changeAnimation('idle','left')

        self.wait_count = 20        # TEMP. As monster behavior gets more complex, find other ways to set timers.
        self.hit_points = None
        self.weapon = None

    def monster_init(self, name):
        """ m.monster_init( str ) -> None

        Use the monster's name as a string key to set values like hit points.
        Might move this to a new MonsterFactory class if it clutters up this 
        class too much.
        """
        if name in MONSTER_DATA_MAP:
            monster_map = MONSTER_DATA_MAP[name]
        else:
            monster_map = MONSTER_DATA_MAP[DEFAULT]
        if HIT_POINTS in monster_map:
            start_hp = monster_map[HIT_POINTS]
        else:
            start_hp = MONSTER_DATA_MAP[DEFAULT][HIT_POINTS]
        if WEAPON in monster_map:
            weapon = monster_map[WEAPON]
        else:
            weapon = MONSTER_DATA_MAP[DEFAULT][WEAPON]
        self.hit_points = [start_hp, start_hp]
        self.weapon = weapon

    #TODO: make this general in the long run, so that monsters can interact with each other as well as with the player.
    #  in particular, consider having monsters "collide" with each other (they probably shouldn't bounce but I'm not sure.)
    def update(self, player):
        """ m.update( Player ) -> None

        The monster's update method depends on what kind of monster it is.
        In the future we should probably do this with a dict.
        """
        self.updateAnimation()
        #TODO: check if the monster can see the player. (using sightdist)
        #TODO: check if the monster is hostile the player.
        #TODO: figure out a better way to assosciate the monster with its udpate action (probably a dict, though name alone might not be sophisticated enoough.)
        if not self.active:
            return
        if self.name == "bat": #TEMPORARY
            self.bat_update(player)
        elif self.name == "giant_frog": #TEMPORARY
            self.frog_update(player)
        elif self.name == "miner":
            self.miner_update(player) #TEMPORARY
        Being.updatePosition(self)

    def set_active(self, active):
        """ m.set_active( bool ) -> None

        Activate or inactivate this monster. This might be pointless since "hurrdurr setters in python 2014"
        """
        self.active = active

    def bat_update(self, player):
        """ m.bat_update( Player ) -> None 

        In-progress method handling a bat's behavior.
        """
        if self.bounce_count > 0:   #TEMP
            self.bounce()
            return
        target = player.current_tile()
        if(target != None):
            self.moveTowards(player.current_tile())

    def frog_update(self, player):
        """ m.frog_update( Player ) -> None 

        In-progress method handling a giant frog's behavior.
        """
        self.gravityUpdate()
        if self.bounce_count > 0:   #TEMP
            self.bounce()
            return
        self.faceTowards(player.current_tile())
        if self.onGround:
            self.changeAnimation('idle', self.direction_id)
            self.xvel = 0
            #TODO: make the frog try to land on the player.
                # figure out the frog's distance from the player, and calculate the necessary xvel.
                # jump with min(self.max_speed/2, target_speed)
            if self.wait_count <= 0:
                self.jump(self.direction_val*self.max_speed/2, self.max_speed)
            self.wait()

    #TEMP
    def miner_update(self, player):
        self.gravityUpdate()
        if self.bounce_count > 0:   
            self.bounce()
            return
        # TODO?
        if self.onGround:
            #self.changeAnimation('idle', self.direction_id)
            self.xvel = 0
    #TODO: miner boss AI goes here.
        self.miner_swing() # TEST
    
    def miner_swing(self):
        self.changeAnimation('swinging', self.direction_id)
        #self.weapon.activate(0, 0, self.direction_id)

    @staticmethod
    def miner_pick():
        return None

    #TEMP


    def collide(self, xvel, yvel):
        """ m.collide( int, int ) -> None 

        The monster processes all the proper collisions with other objects in the level, currently only including 
        impassable objects like platforms.
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

    def collideExits(self):
        """ m.collideExits( ) -> None

        The monster exits the level if outside of its limits, apparently. I'm not really sure why things work like this for monsters.
        """
        exits = self.current_level.get_exit_blocks()
        for e in exits:
            if pygame.sprite.collide_rect(self, e):
                self.exitLevel(e)
                return

    def wait(self):
        """ m.wait( ) -> None

        Decremet the monster's wait count, but not below 0. This is done to make it wait before taking certain actions.
        """
        if(self.wait_count <= 0): return
        self.wait_count -= 1

        #the jump method could go in Being as well.
    def jump(self, xvel = 0, yvel = 0): #TODO: figure out how a monster's jumping ability is determined.
        """ m.jump( int, int ) -> None

        Jump forward with given xvel and up with given yvel. Currently, only the frog does this.
        """
        self.xvel += xvel
        self.yvel -= yvel
        #self.changeAnimation('jumping',self.direction_id)     #TODO
        self.animation.iter()
        self.wait_count = 25 #TEMP
        self.onGround = False

    def faceTowards(self, target):
        """ m.faceTowards( Being ) -> None

        The monster faces left or right, depending on which direction the target is in.
        This will influence movement and animations.
        """
        current_tile = self.current_tile()
        if(target and current_tile):
            x_dist = target.coordinates()[0] - current_tile.coordinates()[0]
            if x_dist == 0: return
            self.direction_val = x_dist/abs(x_dist)
            #TEMP
            if self.direction_val == -1:
                self.direction_id = 'left'
            if self.direction_val == 1:
                self.direction_id = 'right'

    def gravityUpdate(self):    #NOTE: could probably make this a lot more general. (i.e., different terminal velocites for some monsters)
        """ m.gravityUpdate( ) -> None

        The monster falls faster the longer it is in the air because this method increments its yvel.
        However, it will eventually hit terminal velocity.
        """
        if not self.onGround:    # only accelerate with gravity if in the air
            self.yvel += 0.3
            if self.yvel > 100: self.yvel = 100

    def take_damage(self, damage):
        """ m.take_damage( int ) -> None

        The monster takes the given amount of damage, dying if its HP falls below zero.
        """
        if damage <= 0: return
        self.hit_points[0] -= damage
        if self.hit_points[0] <= 0: self.die()

    def die(self):
        """ m.die( ) -> None

        An unfinished method to be called when the monster dies.
        """
        self.delete()
        #TODO: death animation goes here

DEFAULT = "default"
BAT = "bat"
GIANT_FROG = "giant_frog"
MINER = "miner"

HIT_POINTS = "hit_points"
WEAPON = "weapon"

MONSTER_DATA_MAP = { 
    DEFAULT:
        {
        HIT_POINTS:1,
        WEAPON:None
        },
    GIANT_FROG:
        {
        HIT_POINTS:3
        },
    MINER:
        {
        HIT_POINTS:20,
        WEAPON:Monster.miner_pick
        }
}