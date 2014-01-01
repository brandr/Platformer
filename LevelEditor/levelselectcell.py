import guicomponent
from guicomponent import *

class LevelSelectCell(GuiComponent):
	def __init__(self,x,y,width,height):#TODO: args specific to LevelSelectCells 
		GuiComponent.__init__(self,x,y,width,height)
		self.name = "Level 1"	#TODO:specify which level (consider retrieving frm self.level_data)
		#self.addText("Level 1:",22,DEFAULT_MARGIN/8,DEFAULT_MARGIN/8) #TODO: consider 
		self.level_data = None		#TODO: a new level select cell should create a new levelData data member (have to define this class)
		self.initializeButtons()
		
		#TODO: rename level button (make this first since it should be the easiest)
			#will have to truncate long names upon displaying them
		#TODO: edit level button
		#TODO: resize level button
		#button args: (self,image,x,y,effect,*effect_args):

	def update(self):
		GuiComponent.update(self)
		level_name_image = Button.text_component(self.name,22,BLACK)
		self.image.blit(level_name_image,(DEFAULT_MARGIN/8,DEFAULT_MARGIN/8))

	def initializeButtons(self):
		rename_level_button = LevelSelectCell.rename_level_button(self.level_data)
		edit_level_button = LevelSelectCell.edit_level_button(self.level_data)
		resize_level_button = LevelSelectCell.resize_level_button(self.level_data)
		
		self.insert(rename_level_button)
		self.insert(edit_level_button)
		self.insert(resize_level_button)

	@staticmethod
	def rename_level_button(level_data):
		button_image = Surface((DEFAULT_MARGIN*2,DEFAULT_MARGIN-8))
		button_image.fill(Color("#FFFF66"))
		effect = None
		effect_args = 1,
		#TODO
		button = Button(button_image,DEFAULT_MARGIN*2.25,DEFAULT_MARGIN/8,effect,*effect_args)
		button.addText("RENAME",18,DEFAULT_MARGIN/8,DEFAULT_MARGIN/8)
		return button

	@staticmethod
	def edit_level_button(level_data):
		button_image = Surface((DEFAULT_MARGIN*2,DEFAULT_MARGIN-8))
		button_image.fill(Color("#FFFF66"))
		effect = None
		effect_args = 1,
		#TODO
		button = Button(button_image,DEFAULT_MARGIN*4.5,DEFAULT_MARGIN/8,effect,*effect_args)
		button.addText("EDIT",18,DEFAULT_MARGIN/8,DEFAULT_MARGIN/8)
		return button

	@staticmethod
	def resize_level_button(level_data):
		button_image = Surface((DEFAULT_MARGIN*2,DEFAULT_MARGIN-8))
		button_image.fill(Color("#FFFF66"))
		effect = None
		effect_args = 1,
		#TODO
		button = Button(button_image,DEFAULT_MARGIN*6.75,DEFAULT_MARGIN/8,effect,*effect_args)
		button.addText("RESIZE",18,DEFAULT_MARGIN/8,DEFAULT_MARGIN/8)
		return button
		#TODO