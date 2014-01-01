import guicomponent
from guicomponent import *
import scrollbutton
from scrollbutton import *

class  ScrollPane(GuiComponent):
	def __init__(self, x,y,dimensions,window_dimensions,contents,bg = WHITE):
		GuiComponent.__init__(self,x,y,dimensions[0],dimensions[1],bg)
		self.contents = contents
		self.x_window_pos,self.y_window_pos = (0,0) #determine the point on contents that should be in the upper left corner of displayed section
		self.window_width,self.window_height = window_dimensions[0], window_dimensions[1]
		self.scroll_buttons = self.get_scroll_buttons()

	def update(self):
		self.contents.update()
		content_window = self.contents.get_window_at(self.x_window_pos,self.y_window_pos,self.window_width,self.window_height)
		self.image.blit(content_window,(DEFAULT_MARGIN,DEFAULT_MARGIN))
		self.draw_content_border()
		self.update_scroll_buttons()

	def update_scroll_buttons(self):
		if(self.scroll_buttons == None): return
		horizontal_scroll_room = self.horizontal_scroll_room()
		vertical_scroll_room = self.vertical_scroll_room()
		for b in self.scroll_buttons:
			scroll_checks = self.check_scrolling(self.contents)
			scroll_x,scroll_y = scroll_checks[0],scroll_checks[1]
			b.update(scroll_x,scroll_y)
			self.image.blit(b.image,(b.x,b.y))
			#TODO: grey out scroll buttons if we cannot scroll further in a direction.
			#TODO: remove scroll buttons if the contents are resized so that they now fit within the window on one or both axes.
			#TODO: add scroll buttons back in if the contents are resized so that they no longer fit within the window on or both axes

	def horizontal_scroll_room(self): #check if there is room to scroll left/right.
		left_room = (self.x_window_pos > 0)
		right_room = (self.x_window_pos <= self.contents.width)

	def vertical_scroll_room(self):
		up_room = (self.y_window_pos > 0)
		down_room = (self.y_window_pos <= self.contents.height)

	def draw_content_border(self):
		p1 = (self.contents.x,self.contents.y)		#upper left corner
		p2 = (self.contents.x + self.window_width, self.contents.y) #upper right corner
		p3 = (self.contents.x,self.contents.y+self.window_height)		#lower left corner
		p4 = (self.contents.x  + self.window_width, self.contents.y + self.window_height) #lower right corner
		pygame.draw.line(self.image,BLACK,p1,p2)
		pygame.draw.line(self.image,BLACK,p1,p3)
		pygame.draw.line(self.image,BLACK,p2,p4)
		pygame.draw.line(self.image,BLACK,p3,p4)

	def scroll(self,direction,magnitude):
		x_max,y_max = self.contents.width - self.window_width,self.contents.height-self.window_height
		self.x_window_pos = max(0,min(x_max,self.x_window_pos + magnitude*direction[0]))
		self.y_window_pos = max(0,min(y_max, self.y_window_pos + magnitude*direction[1]))

	def button_at(self,pos):
		if(self.scroll_buttons != None):
			for b in self.scroll_buttons:
				if b.contains(pos):
					return b
		relative_pos = self.contents.relative_pos(pos)
		return self.contents.button_at(pos)
		
	def get_scroll_buttons(self):#,scroll_x,scroll_y):
		#if(not (scroll_x or scroll_y)):
		#	return None
		buttons = []
		button_image = ScrollPane.default_button_image()
		greyed_button_image = ScrollPane.default_button_image(True)
		offset_x,offset_y = DEFAULT_MARGIN,DEFAULT_MARGIN
		window_width,window_height = self.window_width,self.window_height

		left_button_image = pygame.transform.rotate(button_image,90)
		left_greyed_button_image = pygame.transform.rotate(greyed_button_image,90)

		right_button_image = pygame.transform.rotate(button_image,270)
		right_greyed_button_image = pygame.transform.rotate(greyed_button_image,270)

		left_button = ScrollButton(left_button_image,left_greyed_button_image,self,LEFT,(offset_x/3), (offset_y/1.25 + self.window_height/2))
		right_button = ScrollButton(right_button_image,right_greyed_button_image,self,RIGHT,offset_x*1.25 + self.window_width,offset_y/1.25+self.window_height/2)
		buttons.append(left_button)
		buttons.append(right_button)
		
		up_button_image = button_image
		up_greyed_button_image = greyed_button_image

		down_button_image = pygame.transform.rotate(button_image,180)
		down_greyed_button_image = pygame.transform.rotate(greyed_button_image,180)

		up_button = ScrollButton(up_button_image,up_greyed_button_image,self,UP,offset_x/1.25 + self.window_width/2,offset_y/3)
		down_button = ScrollButton(down_button_image,down_greyed_button_image,self,DOWN,offset_x/1.25 + self.window_width/2,offset_y*1.25+self.window_height)
		buttons.append(up_button)
		buttons.append(down_button)
		return buttons

	def check_scrolling(self,contents): #find out what kind of scrolling is necessary
		#window_x,window_y = self.content_window_dimensions()[0],self.content_window_dimensions()[1]
		scroll_x = (self.window_width < contents.width)#horizontal scrolling if content width too high
		scroll_y = (self.window_height < contents.height)#vertical scrolling if content height too high 
		return scroll_x,scroll_y

		#TODO: move this fuction to scrollbutton and consider making it take a color arg.
	@staticmethod
	def default_button_image(greyed = False):
		button_image = Surface((DEFAULT_MARGIN/2,DEFAULT_MARGIN/2))
		button_image.fill(WHITE)
		p1 = (DEFAULT_MARGIN/4,0)
		p2 = (0,DEFAULT_MARGIN/2)
		p3 = (DEFAULT_MARGIN/2,DEFAULT_MARGIN/2)
		points = (p1,p2,p3)
		button_color = Color("#FF0000")
		if(greyed):
			button_color = Color("#FF9999")
		pygame.draw.polygon(button_image, button_color, points)
		return button_image

	

	#def content_window_dimensions(self):
	#	return (self.width-2*DEFAULT_MARGIN,self.height-2*DEFAULT_MARGIN)
		#TODO: define a container for contents based on their size
			