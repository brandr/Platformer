""" An invisible trigger that will cause a cutscene to play if the player comes into contact with it and hasn't seen the cutscene yet.
"""

from block import *
from cutscenescripts import MASTER_CUTSCENE_MAP
class CutsceneTrigger(Block):
	""" CutsceneTrigger( AnimationSet, int, int ) -> CutsceneTrigger

	TODO

	Attributes:

	cutscene_key: A string key uniquely associating this trigger with some cutscene.
	"""
	def __init__(self, animations, x, y):
		Block.__init__(self, animations, x, y)
		self.is_square = False
		self.x_interactable = False
		self.is_solid = False
		self.cutscene_key = None

	def update(self, player):
		""" ct.update( Player ) -> None

		TODO
		"""
		if pygame.sprite.collide_rect(self, player) and not player.has_viewed_cutscene(self.cutscene_key) and self.cutscene_key:
			cutscene_script = MASTER_CUTSCENE_MAP[self.cutscene_key]
			# TODO: actually activate the cutscene by reading from cutscenescripts.py
			player.viewed_cutscene_keys.append(self.cutscene_key)
			print self.cutscene_key