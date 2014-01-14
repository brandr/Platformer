import dungeoneditorscreen
from dungeoneditorscreen import *


#can currently read/write dungeons to and from files. Still need to optimize the process and test for bugs, however.

#TODO: make the process of opening the level editor less laggy.
	#the bulk of the lag happens in levelgrid.py, in the addRoom and addEmptyRoom methods.
	#IDEA: replace the grid with a large image, which has gridlines blitted over it with each updates.
		#instead of updating the image/entity data for actual tile cells, simply: 
			#1. add the entity data to a double (string?) array (None to signify empty)
			#2. blit the associated image at the corresponding postion in the grid image.

#TODO: Trim the room sets in DungeonData, preferrably upon its creation if possible.
	 # This means having the roomdata array start at 0,0 and end at the last non-empty room
	 # contained in the dungeondata object.

#TODO: once the leveleditor is a little easier to use, test making multiple connected levels and navigating between them in the game.

#TODO: make the tiledatas created through the leveleditor correspond more closely with the entites than can actually be created in the game.
	# i.e., get entity sets (monster,platforms, etc) from filepaths or something
	# use the same images/image sets when building the level as when playing the game (with some exceptions, like player start position)

#TODO: make it possible to add entities to the leveleditor which take up more than 1 tile (will need some kind of dimensions arg)

#TODO: plan out how tiles, entities, images, animated sprites, etc will all be stored in relation to the Dungeon Editor and the game launcher.

#TODO: delete level button
	#once this is working, I will have to figure out how level deletion translates to the dungeon grid.
		#either the deleted level's rooms should become empty, or they should simply become ununused but not empty.

#TODO: make clicking in the level editor more accurate. (might require in-depth testing)

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