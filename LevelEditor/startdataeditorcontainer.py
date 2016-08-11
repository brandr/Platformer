from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

class StartDataEditorContainer(Box):
	def __init__(self, position, dimensions):
		Box.__init__(self, dimensions[0], dimensions[1])
		self.topleft = (position[0], position[1])
		editor_label = Label("Start Data")
		#TODO: components
		self.add_child(editor_label)
