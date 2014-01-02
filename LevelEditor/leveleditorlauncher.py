import dungeoneditorscreen
from dungeoneditorscreen import *
#TEMPORARY



#TODO: use ocempgui to reproduce current level editor screen fuctionality.

#button = Button ("Hello World")
#button.topleft = (10, 10)
#re.add_widget (button)

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