""" A special kind of tiledata specific to NPCs"""

from tiledata import *

class NPCData(TileData):
	""" NPCData( str, str, str ) -> NPCData

	A special type of tiledata used to generate NPCs.

	Attrbitues:

	Attrbitues:

	text_panes: A list of strings where each element represents a line of text.
	There can be 4 lines at most.
	"""

	def __init__(self, key, filepath, filepath_start = "./"):
		TileData.__init__(self, key, filepath, filepath_start)
		self.file_key = (filepath.split('/')[-1]).split('.bmp')[0] # needed for NPCs to load their animations.
		self.text_panes = [
			["", "", "", ""]
		]
		#self.contents_key = None

	def create_copy(self):
		""" npcd.create_copy( ) -> NPCData

		Create a chestdata that is identical to this one. This is essentially a deep copy.
		This is used in the level editor to copy chests from a template.
		"""
		copy_npc = NPCData(self.entity_key, self.image_filepath)
		copy_npc.text_panes = []
		for i in range(len(self.text_panes)):
			copy_npc.text_panes.append([])
			for line in self.text_panes[i]:
				copy_npc.text_panes[i].append(line)
		return copy_npc

	def formatted_data(self):
		""" npcd.formatted_data( ) -> ( str, str, int, int, ? )

		Format this NPCdata into primitive types so that it can be saved to a file.
		"""
		#TODO: figure out how more complex NPCs will store their contents
		return (self.entity_key, self.image_filepath, self.width, self.height, self.text_panes)

	def set_dialog_text(self, text_panes):
		self.text_panes = text_panes