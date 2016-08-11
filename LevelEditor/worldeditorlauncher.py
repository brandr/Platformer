import pygame
from worldeditorscreen import *

def load_world_editor():
	pygame.init()
	print "Loading world editor..."
	world_renderer = Renderer()
	world_renderer.create_screen(WORLD_WIN_WIDTH, WORLD_WIN_HEIGHT)
	world_renderer.title = "World Editor"
	world_renderer.color = (250, 250, 250)
	world_renderer_screen = WorldEditorScreen(world_renderer)
	world_renderer_screen.openWorldEditor() #add more args if necessary

if __name__ == "__main__":
	load_world_editor()