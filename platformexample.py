import gamescreen
from gamescreen import *

#PLATFORMEXAMPLE (name will probably change):
    #this is currently the only class with a main method, so you can run the game from it.
    #currently the data for building the dungeon is read in from here, though that is likely to change as
        #the data gets more complicated.

def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)

    #NOTE: dungeon map must have all columns the same size and all rows the same size (so perfectly rectangular)
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
    
if __name__ == "__main__":
    main()