import dungeoneditorscreen
from dungeoneditorscreen import *


#TODO: make a dungeon editor that can be used to edit levels and rooms in the dungeon.
	#the end goal is to allow the editor to read/write DungeonData objects to/from files.
		#DungeonData objects are made up of LevelData objects, along with other data about the dungeon.
		#LevelData objects are made up of RoomData objects, along with other data about the level.
		#RoomData objects contain information about tiles and entities in the room, which might be stored 
			#as "TileData" and "EntitiyData" or something like that. I'm not sure yet.
#TODO: delete level button (NICK)
	#once he gets this working, I will have to figure out how level deletion translates to the dungeon grid.
		#somehow, all of the deleted level's rooms should become empty.
#IDEA: consider planning out the entire editors' GUI ahead of time and simply making components with TODOs on them,
	# to show where everything should go. (ROBERT)
#TODO: figure out how to open the level editor for a level that already has rooms. (will have to define room data first)
#TODO: decide whether or not we actually need a "resize level" button,since levels are currently resizable.
#TODO: make the actual level Editor.
	#currently, this is a separate window that pops up when the "Edit Level" button is clicked.
	#need to make it possible to add platforms, enemies, lanterns, etc.
		#in the long run, all of these should be loaded from some kind of library.
		#might end up moving the folder that currently holds sprite data into the LevelEditor folder
#TODO: conisder whether room data should be wiped when a level is deleted or resized (and if not, how it should be handled).
	#IDEA: a special state for rooms which are deselected and not empty, but have no corresponding level.
		#(might need to rename the "deselected" state for clarity.)
#IDEA: make it clear somehow which levels are empty (no rooms) in the LevelSelectContainer.
	#could grey out the names of these levels
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

	#level_renderer = Renderer()
	#level_renderer.create_screen(LEVEL_WIN_WIDTH,LEVEL_WIN_HEIGHT)
	#level_renderer.title = "Level Editor"
	#level_renderer.color = (250,250,250)

	dungeon_editor_screen = DungeonEditorScreen(dungeon_renderer)#,level_renderer)
	dungeon_editor_screen.openDungeonEditor() #add more args if necessary

if __name__ == "__main__":
	loadMapEditor()