from gameimage import GameImage
from leveleffect import LevelEffect

class LevelEffectFactory:
	""" No constructor.
	"""
	@staticmethod
	def build_entity(animation_set, effect_data, x, y):	#not sure if I can use sign_key-- might need a different structure to figure out the proper text
		""" build_entity( Surface, Rect, LevelEffectData, int, int ) -> LevelEffect

		Create a LevelEffect using the correct data.
		"""
		for direction in animation_set.animations:
			for key in animation_set.animations[direction]: animation_set.animations[direction][key].set_all_alphas(effect_data.transparency)
		effect = LevelEffect(animation_set, x, y)
		return effect