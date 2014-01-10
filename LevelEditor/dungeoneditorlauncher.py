import dungeoneditorscreen
from dungeoneditorscreen import *


#can currently read/write dungeons to and from files, though there are some minor problems.

#TODO: decide whether empty levels  should actually be deleted. (probably not since it might be useful to make placeholders)
#TODO: call some kind of update methods for the level/dungeon screens so that there is no current level selection, and make sure
	#this is represented in the GUI.
#TODO: make saving/loading (mostly loading) levels less laggy. (may need some print tests to pinpoint where the bulk of the lag is coming from.)
	#IDEA: could resize the dungeonData to only include a rectangular area containing all of the nonempty rooms
		#if this proves difficult, we may need to keep track of the overall dungeon dimensions via the dungeon grid, and store this info in dungeondata.

#TODO: now that the level editor can read/write correctly, create an actual test dungeon for playing the game.
	  #1. keep track of the starting level (and that level's starting tile) as the dungeon is built. 
	  	#Alternately, just let the dungeon factory determine this by finding the corresponding tile object as it reads the tiles.
	 	#since the player is larger than a tile, the "player start" tile data should "block out" the tile below it 
	 		#(and therefore be impossible to place at the bottom of the screen).
	 		#Think of a general way of placing entites into the level editor, given dimensions greater than 1 tile.
	  #2. Make sure the dungeon factory used to launch the game can properly import DungeonData, along with the 
	  	# static dungeonDataFromFile method in filemanagercontainer.py.
	  #3. figure out how tiles will be set (as oppossed to actual entities)

#TODO: delete level button
	#should probably just do this myself
	#once this is working, I will have to figure out how level deletion translates to the dungeon grid.
		#either the deleted level's rooms should become empty, or they should simply become ununused but not empty.

#TODO: make the process of opening the level editor less laggy.

#TODO: make clicking in the level editor more accurate. (might require in-depth testing)

#TODO: decide whether or not we actually need a "resize level" button,since levels are already resizable.

#TODO: Flesh out the actual level Editor.
	#make it possible to have more than 2 layers of entity selection.

#NOTE: might end up moving the folder that currently holds sprite data into the LevelEditor folder

#IDEA: give the dungeon grid container a color key explaining what the six different colors mean.

#IDEA: make it clear somehow which levels are empty (no rooms) in the LevelSelectContainer (not the dungeon grid).
	#could grey out the names of these levels
	#could also find a way to represent levels which contain rooms, but whose rooms have no tile data.

#IDEA: a button to move a level (or set of levels, which would be much more complicated) 
	#while also moving the rooms inside the level.
		#i.e., the level itself would not change at all, but simply be in a different part of the dungeon.

#IDEA: a quick way of deleting everything in each room of a level without deleting or resizing the level itself.

#IDEA: make the deselected color of a dungeon grid tile correspond to its associated level's color.
	#A level's color would be set by the user.
	
#IDEA: in the level editor, consider axis labels for the level grid to number rooms/tiles by their coords.

#Other classes in this folder will not be used in the final version of this gui,
	#unless they are heavily rewritten. Do not delete unused classes yet, though,
	#because it may be useful to look at them to copy their functionality.

def loadMapEditor():
	pygame.init()
	
	dungeon_renderer = Renderer()
	dungeon_renderer.create_screen(DUNGEON_WIN_WIDTH,DUNGEON_WIN_HEIGHT)
	dungeon_renderer.title = "Dungeon Editor"
	dungeon_renderer.color = (250, 250, 250)

	dungeon_editor_screen = DungeonEditorScreen(dungeon_renderer)
	dungeon_editor_screen.openDungeonEditor() #add more args if necessary

if __name__ == "__main__":
	loadMapEditor()