import entity
from entity import *

class ExitBlock(Entity): #block which exits the level and takes the player elsewhere
	def __init__(self, animations,x, y):
		Entity.__init__(self,animations)#Rect(x, y, 32, 32))
		self.color = Color("#0000FF")
		self.rect = Rect(x, y, 32, 32)

	def update(self, player): 
		pass