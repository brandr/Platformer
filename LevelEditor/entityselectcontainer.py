from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

from tiledata import *

MAX_ENTITY_WINDOWS = 4
BMP_FILETYPE = 33204 #not sure if this will work cross-platform. (Then again, a lot of this game might not.)

#TODO: instead of showing current entity image in the pane, blit current entity image over a white square the size of max-sized image.

class EntitySelectContainer(Box): #window might not be the right name anymore.
	"""docstring for EntitySelectContainer"""
	def __init__(self, width, height):
		Box.__init__(self,width,height)

		self.current_entity = None
		self.entity_select_window = self.entity_select_window(200,240,0,0)
		self.current_entity_label = Label("Current Entity Sprite: None")
		self.current_entity_label.topleft = self.entity_select_window.left,self.entity_select_window.bottom+8
		
		self.current_entity_image = EntitySelectContainer.blank_entity_image()
		self.current_entity_image.topleft = self.current_entity_label.left,self.current_entity_label.bottom+8

		self.add_child(self.entity_select_window)
		self.add_child(self.current_entity_label)
		self.add_child(self.current_entity_image)

	def entity_select_window(self,width,height,x,y): #TODO
		file_list = FileList (width, height, "./images")
		file_list.topleft = x,y
		file_list.connect_signal(SIG_SELECTCHANGED,self.change_selection,file_list)
		return file_list

	def change_selection(self,file_list):

		def is_bmp(filename):
			extension = filename[-4:]
			return extension == ".bmp"

		file_list_item = file_list.get_selected()[0]
	#print file_list_item.filetype
		if(not is_bmp(file_list_item._text)): 
			self.select_entity()
			return

		self.select_entity(file_list._directory,file_list_item._text)

	def select_entity(self,directory = None,file_key = None):
		#TODO: expand current entity label to indicate both the entity itself and the sprite.
		if file_key == None: #not key in SELECTABLE_ENTITY_MAP:
			self.current_entity = None
			self.updateCurrentEntityImage()
			self.current_entity_label.set_text("Current Entity Sprite: None")
			return
		filepath = "/"+directory+"/"+file_key
		tile_key = (directory.split('/'))[-1]
		self.current_entity = TileData(tile_key,filepath)
		self.current_entity_label.set_text("Current Entity Sprite: "+file_key) 
		self.updateCurrentEntityImage()

	def updateCurrentEntityImage(self):
		if(self.current_entity == None): 
			blank_square = Surface((32,32)) #TODO: needs to be larger once current entity can be larger.
			blank_square.fill(Color("#FFFFFF"))
			self.current_entity_image.set_picture(blank_square)
			return
		image = self.current_entity.get_image()
		self.current_entity_image.set_picture(image)

	def open_entity_window(self,layer,collection):
		window = ScrolledList(self.width/MAX_ENTITY_WINDOWS,self.height/2)
		window.left += (layer-1)*(self.width/MAX_ENTITY_WINDOWS)
		window.set_items(collection)
		window.set_selectionmode(SELECTION_SINGLE)
		window.connect_signal(SIG_SELECTCHANGED,self.change_selection,layer,window)
		if(self.entity_windows[layer] != None):
			for n in range (layer,MAX_ENTITY_WINDOWS+1):
				self.close_entity_window(n)
		self.entity_windows[layer] = window
		self.add_child(window)

	def close_entity_window(self,layer):
		if layer >= len(self.entity_windows) or self.entity_windows[layer] == None: return
		self.remove_child(self.entity_windows[layer])
		self.entity_windows[layer].destroy()
		self.entity_windows[layer] = None

	def current_image(self):
		return self.current_entity_image.picture

	@staticmethod
	def primary_entity_collection():
		collection = ListItemCollection()
		for item_name in PRIMARY_ENTITY_NAMES:
			collection.append(TextListItem(item_name))
		return collection

	@staticmethod
	def entity_collection(name_set):
		collection = ListItemCollection()
		for item_name in name_set:
			collection.append(TextListItem(item_name))
		return collection

	@staticmethod
	def blank_entity_image():
		blank_square = Surface((32,32)) #TODO: needs to be larger once current entity can be larger.
		blank_square.fill(Color("#FFFFFF"))
		return ImageLabel(blank_square)