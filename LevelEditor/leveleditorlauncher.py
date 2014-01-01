import leveleditorscreen
from leveleditorscreen import *

#TODO: use ocempgui to reproduce current level editor screen fuctionality.

#TEMPORARY
from ocempgui.widgets import *

# Initialize the drawing window.
re = Renderer ()
re.create_screen (100, 50)
re.title = "Hello World"
re.color = (250, 250, 250)

button = Button ("Hello World")
button.topleft = (10, 10)
re.add_widget (button)

# Start the main rendering loop.
re.start ()

def loadMapEditor():
	pass
	#pygame.init()
	#screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH) #might want to change these args
	#level_editor_screen = LevelEditorScreen()
	#level_editor_screen.openEditor(screen) #add more args if necessary
#if __name__ == "__main__":
	#loadMapEditor()