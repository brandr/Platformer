from levelgrid import *

class LevelGridWindow(ScrolledWindow):
	def __init__(self,level_editor,x,y,width,height):
		ScrolledWindow.__init__(self,width,height)
		self.topleft = x,y
		self.level_grid = LevelGrid(level_editor,16,16)
		self.set_child(self.level_grid)
		self.master_editor = level_editor
		self.connect_signal(SIG_MOUSEDOWN,self.level_grid.processClick,self.calculate_offset) #TEMP (but will probably connect this signal here)

	def setLevelData(self,data):
		self.level_grid.setLevelData(data)

	def calculate_offset(self):
		window_pos = (self.left,self.top)
		x_scroll_offset = self.hscrollbar.value
		y_scroll_offset = self.vscrollbar.value
		container = self.master_editor
		container_offset = (container.left,container.top)
		master_window = container.master_window
		master_window_offset = (master_window.left,master_window.top)
		caption_bar_height = master_window._captionrect.height
		x_total_offset = master_window_offset[0]+container_offset[0]+window_pos[0] - x_scroll_offset
		y_total_offest = master_window_offset[1]+container_offset[1]+window_pos[1] - y_scroll_offset+caption_bar_height
		return (x_total_offset,y_total_offest)