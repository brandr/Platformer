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
#TODO: conisder whether room data should be wiped when a level is deleted or resized (and if not, how it should be handled).
	#consider a special state for rooms which are deselected and not empty, but have no corresponding level.
		#(might need to rename the "deselected" state for clarity.)
#TODO: consider a button to move a level (or set of levels, which would be much more complicated) 
	#while also moving the rooms inside the level.
		#i.e., the level itself would not change at all, but simply be in a different part of the dungeon.
#IDEA: consider a quick way of deleting everything in each room of a level without deleting or resizing the level itself.
#IDEA: make the deselected color of a dungeon grid tile correspond to its associated level's color.
	#A level's color would be set by the user.

#Other classes in this folder will not be used in the final version of this gui,
	#unless they are heavily rewritten. Do not delete unused classes yet, though,
	#because it may be useful to look at them to copy their functionality.

def loadMapEditor():
	pygame.init()
	
	#screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH) #might want to change these args
	renderer = Renderer()
	renderer.create_screen(WIN_WIDTH,WIN_HEIGHT)
	renderer.title = "Dungeon Editor"
	renderer.color = (250, 250, 250)

	dungeon_editor_screen = DungeonEditorScreen(renderer)
	dungeon_editor_screen.openEditor() #add more args if necessary

if __name__ == "__main__":
	loadMapEditor()