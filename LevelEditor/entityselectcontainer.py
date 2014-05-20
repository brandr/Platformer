from tiledata import *
from ocempgui.widgets import Bin, Box, FileList, Label, ImageLabel, Label, Entry
from ocempgui.widgets.BaseWidget import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *

MAX_ENTITY_WINDOWS = 4
BMP_FILETYPE = 33204 #not sure if this will work cross-platform. (Then again, a lot of this game might not.)

#TODO: instead of showing current entity image in the pane, blit current entity image over a white square the size of max-sized image.

class EntitySelectContainer(Box):
	"""docstring for EntitySelectContainer"""
	def __init__(self, width, height):
		Box.__init__(self, width, height)

		self.current_entity = None
		self.entity_select_window = self.entity_select_window(100, 240, 0, 0)
		self.current_entity_label = Label("Current Entity Sprite: None")
		self.current_entity_label.topleft = self.entity_select_window.left, self.entity_select_window.bottom + 8 
		
		self.current_entity_image = EntitySelectContainer.blank_entity_image()
		self.current_entity_image.topleft = self.current_entity_label.left, self.current_entity_label.bottom + 8

		#self.additional_entity_data_pane = self.additional_entity_data_pane(340, 240, self.entity_select_window.right + 8, self.entity_select_window.top) #TODO: make this method and get dimensions right
		#TODO: make a greyed-out scrolledlist that selects "additional data" from some file (to be used for sign text)
		# may want this to be its own class
		# alternately, open up a mini-version of the sign and allow text to be typed directly on it (should definitely be its own class)

		self.add_child(self.entity_select_window)
		self.add_child(self.current_entity_label)
		self.add_child(self.current_entity_image)
		#self.add_child(self.additional_entity_data_pane)

	def entity_select_window(self, width, height, x, y): #TODO
		file_list = FileList (width, height, "./images")
		file_list.topleft = x, y
		file_list.connect_signal(SIG_SELECTCHANGED, self.change_selection, file_list)
		return file_list

	def change_selection(self, file_list):
		def is_bmp(filename):
			extension = filename[-4:]
			return extension == ".bmp"

		file_list_item = file_list.get_selected()[0]
		if(not is_bmp(file_list_item._text)): 
			self.select_entity()
			return

		self.select_entity(file_list._directory, file_list_item._text)

	def select_entity(self, directory = None, file_key = None):
		#TODO: deciding whether additional data can be set should probably happen here
		if file_key == None: #not key in SELECTABLE_ENTITY_MAP:
			self.current_entity = None
			self.updateCurrentEntityImage()
			self.current_entity_label.set_text("Current Entity Sprite: None")
			return
		filepath = "/" + directory + "/" + file_key
		tile_key = (directory.split('/'))[-1]
		tile_key = (tile_key.split('\\'))[-1]
		self.current_entity = TileData(tile_key, filepath)
		self.current_entity_label.set_text("Current Entity Sprite: " + file_key) 	# May want to update additional_entity_data_pane only when an object is placed, not when its template is selected. k
		#self.additional_entity_data_pane.update_data(tile_key, self.current_entity) # NOTE: current_entity needs to be a specific sign instance, not a sign template. Change this.
		self.updateCurrentEntityImage()												# Also, make it possible to select objects in the level grid instead of just placing them.

	def updateCurrentEntityImage(self):
		if(self.current_entity == None): 
			blank_square = Surface((32, 32)) #TODO: needs to be larger once current entity can be larger.
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
			for n in range (layer, MAX_ENTITY_WINDOWS + 1):
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

	#def additional_entity_data_pane(self, width, height, x, y):
	#	data_pane = EntityDataPane(width, height)
	#	data_pane.topleft = x, y
		#data_pane.set_child(data_pane.current_contents)
		#file_list.connect_signal(SIG_SELECTCHANGED, self.change_selection, file_list) #connect to self if necessary
	#	return data_pane