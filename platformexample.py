import gamescreen
from gamescreen import *

    #KNOWN BUGS

#player can end up in a "None" level (and crash game) when leaving a level
    #this can occur with certain combinations of sprinting/jumping while leaving the level.
    #so far it seems to only happen when leaving the level horizontally while jumping and
        #sprinting through a gap of the same height as the player.
    #it's possible that other bugs may occur if the player does this combination of actions, even when not leaving the level.

    #IMMEDIATE STUFF
 
#with new level system, experiment with different level configurations
#separate Room building from LevelFactory into a new RoomFactory class (ROBERT)
#expand levelData into its own class which might include sprite/tile sets, indoors/outdoors, and other data 
    #not necessarily found in Room
    #MOST IMPORTANTLY, consider how levelData might be derived from input
        #in the long run, this input may come from the level editor.
        #consider a set of "level tags" for the editor, as well as
            #different "layers" that can be toggled (i.e.,background layer, platforms layer, and (at dungeon zoom level)
                #a layer which shows which levels contain which rooms)
    #Conisder determining origin from the list of room coords (we want the one with both the lowest x *and* the lowest y)
#fix movement/rect related stuff, and put all relevant methods in gameImage, to be called by subclasses.
    #there seems to be some inconsistency about which parts of rects are moved (left,top,centerx,centery,etc)
#fix imports
#reintroduce outdoor levels (data should be part of levelData)
#consider how background tiles, platform tiles, etc might be reorganized
    #EXAMPLE: could have a tileset 
#consider removing level_ID, but first try to think of possible uses for it.

    #LESS IMMEDIATE STUFF

#rename this class to something besides "platformexample"
#store/organize sprites a little better.
    #keep in mind that we need an extensible way to load sprites, so if they are in different directories
        #we need to plan out how we'll access them.
#build the enemies extensibly. Make temporary classes/methods if necessary, but plan to replace them later
    #have the bat start hanging from the ceiling and maybe give it "dropping"
        #animation followed by the flying animation
    #change the bat's attack patterns so that it periodically flaps around the player before diving, bounces off, 
        #moves away, and then dives again.
        #(some randomness may make this pattern look more natural)
    #make lighting less laggy for large amounts of light
        #one way might be to only udpate tiles within rectangular areas around light sources.
    #consider possible combat systems (damage, HP, etc)

    #SPRITE STUFF

#TODO: organize sprite system better
    #IDEA: make a data structure involving double arrays which allows:
        #1. loading the level
        #2. loading the level editor
        #3. keeping track of animations, tile spritesheets, entity sprites, entities, etc
#TODO: consider having tiles/textures be procedurally generated
       #based on hardcoded platform locations/level data and a library of tiles
       #alternately, use the map editor and a tileFactory to load in tiles from images which represent levels
#TODO: at some point in the program after pygame.display is intiliazed, load all the sprites and store them
        #in a neat, extensible, easily accessible manner. (consider a spritefactory which will probably be
        #related to tilefactory)

        #ENEMY/AI STUFF
#TODO: implement more enemies.
#TODO: when adding AI, try to be creative and extensible, as though this were a roguelike.
#IDEA: could give some monsters strong knockback by increasing the bounce they deliver.
#NOTE: enemies remain in the exact same state they were left in when the player leaves a level. should decide if this is good or bad.

       #LEVEL STUFF
#IDEA: consider an intermediary, constant-sized square area between tile and level. (ala super metroid)
    #player scrolling would not be affected by this area, but would still be affected by level.
    #since this area's size would not vary, it could be useful for dealing with global coords and level connections.
#TODO: consider a level editor
#TODO: handle the case for the player going offscreen where there is no next level.
#TODO: figure out a long-term plan for storing multiple levels.
#IDEA: instead of specifically creating exit blocks beteween level, simply call
        #the same methods to move the player when he hits the edge of the screen,
        #and treat the edge as a block if there is nowhere to go.
#TODO: consider reading in all levels from a single input, with a set level size
        #and exit blocks placed based in open spaces between levels rather than
        #directly placing them (implement that part first)
#TODO: consider making level-linking system more extensible, choosing player's 
        #local coords based on global coords measured on the same scale. 
        #(this might allow for differently-sized levels)
#IDEA: make the level editor "zoomable" so that the entire dungeon can be viewed and
    # levels can be added/moved, but it is also possible to select, expand and edit a specific level.

        #PLATFORM STUFF
#TODO: make the "platform" system more complex, possibly with inheritance/factory
        #consider platforms that  the player can jump up through and/or fall through  by tapping down
#TODO: conider making half-steps and/or slopes that can be walked up

        #MISC STUFF
#TODO: make it possible for the player to open up a map screen.
        # (it may help to first rough out a very general design for "screens", "menus", and "controls"
#TODO: make invisible caverns which can be revealed somehow. (test in sunlight first)
#TODO: give exit blocks super terrifying sprites. (they can't be seen normally so it will be a fun surprise if there's a glitch or something)


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)

    #TODO: try reading in the whole dungeon from one map instead
    dungeon_map = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",#1
        "PPPP           PPPPPPPPPPPPPPPPPP                             PPP                              PP                              P",
        "PPPP           PPPPPPPPPPPPPPPPPP                             PPP                              PP                              P",
        "PPPP           P            PPPPP                             PPP                              PP                              P",
        "PPPP           P            PPPPP                             PPP                              PP                              P",#5
        "P              P            PPPPP                             PPP                              PP                              P",
        "P              P            PPPPP                             PPP                              PP                              P",
        "P              P            PPPPP                             PPP                              PP                              P",
        "P              P            PPPPP                             PPP                              PP                              P",
        "P                           PPPPP                             PPP                              PP                              P",#10
        "P                              PP                             PPP                              PP                              P",
        "P                    PPPP      PP                             PPP                              PP                              P",
        "P                              PP                             PPP                              PP                              P",
        "P                              PP                             PPP                              PP                              P",
        "P                              PP                              PP                              PP                              P",#15
        "P                              PP                              PP       PPPPP                  PP                              P",
        "                       PPPPPPPP         PPPPPPPPPPPPPPPPPP                        PPPP                                         P",
        "        S                                                                                                                      P",
        "                                          L                                                                  L                 P",
        "PPPPPPPPPPPPP  PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPP   PPPPPPPPPP",#20
        "PPPPPPPPPPPPP  PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",#21
        "PPPP           PPPPPPPPPPPPPPPPPP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPP           PPPPPPPPPPPPPPPPPP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPP        PPPP            PPPPP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPP           P            PPPPP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",#25
        "P              P            PPPPP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P              P            PPPPP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P              P            PPPPP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P              P            PPPPP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                           PPPPP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",#30
        "P                              PP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                    PPPP      PP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                              PP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                              PP                             PPP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                              PP                              PP                              PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",#35
        "P                              PP                              PP       PPPPP                  PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P             PPP              PP                                                 PPPP         PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP                                                                                             PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP                  L                     PPPP                                                 PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",#40
    ]  # 1   5    10   15   20   25   30  

    level_1_rooms = [(0,0)]
    level_1_origin = (0,0)
    level_1_data = [1,level_1_origin,level_1_rooms]

    level_2_rooms = [(1,0),(2,0),(3,0)]
    level_2_origin = (1,0)
    level_2_data = [2,level_2_origin,level_2_rooms]

    level_3_rooms = [(0,1),(1,1)]
    level_3_origin = (0,1)
    level_3_data = [3,level_3_origin,level_3_rooms]

    level_4_rooms = [(2,1)]
    level_4_origin = (2,1)
    level_4_data = [4,level_4_origin,level_4_rooms]

    level_data = [level_1_data,level_2_data,level_3_data,level_4_data]

    dungeon = LevelGroup(dungeon_map,level_data)
    mainScreen = GameScreen()
    mainScreen.runGame(screen,dungeon)
   
    #the level maps below here are not being used right now.

    level00 = [
        "PPP                                                                   PPP",
        "PPP                                                                   PPP",
        "PPP                                                                   PPP",
        "PPP                                                                   PPP",
        "PPP                                                                   PPP",
        "PPP                                                                   PPP",
        "PPP                                                                   PPP",
        "PPP                                                                   PPP",
        "PPP                                                                   PPP",
        "PPP                                                         B      PPPPPP",
        "PPP                                                                PPPPPP",
        "PPP                                                                     N",
        "PPP                                                                     N",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPP   PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPNNNNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]

    level01 = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPP  PPPPPPPPPPPPPP PPPPPP",
        "PP     PPPPPPPPPPPPPPPP  PPPPP PPPP  PPPPPPPPPPPP    PP  PPPP  PP  PPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP  PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP      B                                                              PP",
        "N                          S                                            N",
        "N                                L                                      N",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]

    level02 = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPPPP   PPPPPPPPPPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPP",
        "PP     PPPPPPPPPPP    PPPPPPPPPPPPPP PPPPPPPPPPPPP  PPPPPPPPPPPPPP PPPPPP",
        "PP     PPPPPPPPPPPP      PPPPP PPPP  PPPPPPPPPPPP    PP  PPPP  PP  PPPPPP",
        "PPPPPPPPPPPPPPPPP        PPPPPPPPPPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPPPP",
        "PP                                                                    PPP",
        "N                                                                     PPP",
        "N                                                                     PPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]

    level10 = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPLPPPPPPLPPPPP    PP   LPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPP     PPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPL     PPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPP     PPPPPPPPPP    PPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPP     PPPPPPPPPP    PPPP PPPPPPPPPPPPP  PPPPPPPPPPPPPP PPPPPP",
        "PPP    PPPPPP     PPPPP  PPP    PPP  PPPPPPPPPPPP    PP  PPPP  PP  PPPPPP",
        "PPP    PP PPP     PPPP    PP    PPPP PPP   P PPP     PP  PP   PPPP  PPPPP",
        "PPP                                                                    PP",
        "PPP                                                                     N",
        "PPP                                                                     N",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]

    level11 = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPRPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPP PPPPPPPPPPPPP  PPPPPPPPPPPPPP PPPPPP",
        "PPP    PPPPPPPPPPPPPPPP  PPP    PPP  PPPPPPPPPPPP    PP  PPPP  PP  PPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPP PPP   P PPP     PP  PP   PPPP  PPPPP",
        "PPP                                                                    PP",
        "N                                                                       N",
        "N                                                                       N",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]

    level12 = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPRPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPP PPPPPPPPPPPPPPPPPPPPPP",
        "PPP    PPPPPPPPPPPPPPPPPPPPP    PPPP PPPPPPPPPPPPP  PPPPPPPPPPPPPP PPPPPP",
        "PPP    PPPPPPPPPPPPPPPP  PPP    PPP  PPPPPPPPPPPP    PP  PPPP  PP  PPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPP PPP   P PPPPP   PP  PP   PPPP  PPPPP",
        "PPP                                                                   PPP",
        "N                                                                     PPP",
        "N                                                                     PPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]

    #levels_row0 = [level00,level01,level02]
    #levels_row1 = [level10,level11,level12]

    #dungeon_levels = [levels_row0,levels_row1]
    #dungeon = LevelGroup(dungeon_levels)
    
    
if __name__ == "__main__":
    main()