""" A world represents the entire physical area a player can possibly explore, along with some persistent data like morality.
"""

class World:
	""" World( ? ) -> World

	TODO
	"""
	def __init__(self, dungeon):
		#self.dungeon = dungeon
		self.dungeons = [dungeon] #TEMP. need mulitple dungeons, not sure how to get them yet though.
		#self.start_data = ? #TODO
		#TODO: intstead of doing this, grab connected dungeons from this dungeon (maybe only as they are needed though)
#TODO: A whole new woooooooooooooooooorld
