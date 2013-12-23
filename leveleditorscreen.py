import leveleditor
from leveleditor import *

class LevelEditorScreen:

	def __init__(self):
		self.level_editor = LevelEditor((8,8)) #the tuple arg represets the size of the dungeon to be created.

	def openEditor(self,screen):
		pygame.display.set_caption("Level Editor")
		timer = pygame.time.Clock()
		bg = Surface((32,32))
		bg.convert()

		while 1:
			timer.tick(60)
			for e in pygame.event.get():
				self.processEvent(e) #IDEA: do something similar for gamescreen
			for y in range(32):
				for x in range(32):
					screen.blit(bg, (x * 32, y * 32))
			self.level_editor.update(screen)

	def processEvent(self,e):
		if e.type == QUIT: raise SystemExit, "QUIT"
		if e.type == KEYDOWN and e.key == K_ESCAPE:
			raise SystemExit, "ESCAPE"
		#TODO: mouse click events