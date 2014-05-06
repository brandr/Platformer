from block import *

class ExitBlock(Block): #block which exits the level and takes the player elsewhere
	def __init__(self, animations,x, y):
		Block.__init__(self, animations, x, y)#Rect(x, y, 32, 32))
		#self.rect = Rect(x, y, 32, 32)

	def update(self, player): 
		pass