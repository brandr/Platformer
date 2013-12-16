import platform
from platform import *
#consider a gameimage factory, too

class PlatformFactory(object):
	def newPlatform(self,x,y):	#TODO: add args as platforms become more complex
		return Platform(x,y)