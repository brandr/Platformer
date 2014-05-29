import platform
from platform import *
#consider a gameimage factory, too

#seems like I'm not really using this now, but keep it around because I might flesh it out more later.

class PlatformFactory(object):
	def newPlatform(self,x,y):	#TODO: add args as platforms become more complex
		return Platform(x,y)