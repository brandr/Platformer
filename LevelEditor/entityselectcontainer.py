from ocempgui.widgets import *
from ocempgui.widgets.Constants import *
from ocempgui.widgets.components import *
from pygame import *
import pygame, pygame.locals
from ocempgui.draw import Image

MAX_ENTITY_WINDOWS = 4
#TODO: consider associating with more complex data objects than strings for the actual entities. (or just add another dict for those.)
#TODO: Ideally, build these data structures from some input, like a set of files/folders.
PLATFORMS = "platforms"
MONSTERS = "monsters"
PRIMARY_ENTITY_NAMES = (PLATFORMS,MONSTERS)

DEFAULT_PLATFORM,FIRE_PLATFORM = "default_platform","fire_platform"
PLATFORM_NAMES = (DEFAULT_PLATFORM,FIRE_PLATFORM)

BAT,GIANT_FROG = "bat","giant_frog"
MONSTER_NAMES = (BAT,GIANT_FROG)
#MONSTERS = (BAT,GIANT FROG) #could potentially do something like this
PRIMARY_ENTITY_MAP = {PLATFORMS:PLATFORM_NAMES, MONSTERS:MONSTER_NAMES} #could potentially map category names to more maps, rather than name lists.

SELECTABLE_ENTITY_MAP = {DEFAULT_PLATFORM:"default_platform.bmp",FIRE_PLATFORM:"fire_platform.bmp",
						BAT:"bat.bmp", GIANT_FROG:"giant_frog.bmp"}	#TODO: find a good way to organize more data than this, since we want to map to actual objects, not just image filenames.

class EntitySelectContainer(Box): #window might not be the right name anymore.
	"""docstring for EntitySelectContainer"""
	def __init__(self, width, height):
		Box.__init__(self,width,height)
		self.primary_entity_window = self.primary_entity_window()
		self.entity_map = PRIMARY_ENTITY_MAP #there might be a better way to get this via a getter (which would be called contextually)
		self.entity_windows = [] #could put primary entity window here
		for n in xrange(MAX_ENTITY_WINDOWS+1): self.entity_windows.append(None)

		self.current_entity = None

		self.current_entity_label = Label("Current Entity: None")
		self.current_entity_label.topleft = self.primary_entity_window.left,self.primary_entity_window.bottom+8
		self.current_entity_image = EntitySelectContainer.blank_entity_image()
		self.current_entity_image.topleft = self.current_entity_label.left,self.current_entity_label.bottom+8

		self.add_child(self.primary_entity_window)
		self.add_child(self.current_entity_label)
		self.add_child(self.current_entity_image)


		#TODO: add a connect_signal for the entity select window so that when something is selected, it will update:
		#1) an image label showing the image corresponding to the currently selected entity, and
		#2) the actual current seletion, which will affect both visual and data-related changes that occur
			#when a tile is clicked.
			#NOTE: this might not take the form of a connect_signal.

	def primary_entity_window(self): #maybe entity windows should be their own class (unless it is easier to organize some other way.)
		window = ScrolledList(self.width/MAX_ENTITY_WINDOWS, self.height/2)
		entity_collection = EntitySelectContainer.primary_entity_collection()
		window.set_items(entity_collection)
		window.set_selectionmode(SELECTION_SINGLE)
		window.connect_signal(SIG_SELECTCHANGED,self.change_selection,1,window)
		return window

	def change_selection(self,layer,entity_window):
		entity_key = entity_window.get_selected()[0].text
		if entity_key in self.entity_map: #TODO: change this bit to be more extensible by checking layer, text, selection before layer, etc
			name_collection = self.entity_map[entity_key]
			collection = EntitySelectContainer.entity_collection(name_collection)
			self.open_entity_window(layer+1,collection)
			return
		#TODO: this would be a good place to check which entity map we should be using. (unless we have one master map to store all entities, which might wor.)
		self.select_entity(entity_key)

	def select_entity(self,key): #might benefit from layer arg
		if not key in SELECTABLE_ENTITY_MAP:
			self.current_entity = "None" #TEMP. We want to store more data than just the name in the long run. (unless this data can be retrieved with this key later.)
			self.current_entity_label.set_text("Current Entity: None")
			return
		self.current_entity = key #TEMP
		self.current_entity_label.set_text("Current Entity: "+key) #TEMP. need much more to actually place entities.
		self.udpateCurrentEntityImage(key)

	def udpateCurrentEntityImage(self,key):
		if not key in SELECTABLE_ENTITY_MAP: return #might not be the right error action
		filename = SELECTABLE_ENTITY_MAP[key]
		image = Image.load_image ("./images/"+filename) #might not be correct. also, if we have a lot of images, might need a way to specify filepath better.
		self.current_entity_image.set_picture(image)

	def open_entity_window(self,layer,collection):
		#TODO: make more extensible than this (I'm not 100% sure we can open more than two layers, though we might not need to.)
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
		blank_square = Surface((32,32))
		blank_square.fill(Color("#FFFFFF"))
		return ImageLabel(blank_square)