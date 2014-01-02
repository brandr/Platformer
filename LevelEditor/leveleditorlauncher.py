import dungeoneditorscreen
from dungeoneditorscreen import *


#TODO: use ocempgui to reproduce current level editor screen fuctionality.
#currently used classes include:
	#leveleditorlauncher.py
	#dungeoneditorscreen.py
	#levelselectcontainer.py
	#levelselectcell.py

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