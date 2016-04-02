from random import randint

from enum import Enum
from redlib.api.py23 import enum_attr

from ..db.app.config import Config


ImageSelectorMethod = Enum('ImageSelectorMethod', ['random', 'rank', 'score', 'size', 'time'])


class ImageSelector:

	def __init__(self, images, trace):
		self._images = images
		self._trace = trace

		self._filters = []
		self.set_method()


	def set_method(self):
		ism = ImageSelectorMethod
		config = Config()
		method = ism.rank or enum_attr(ism, config.eget('image.selection_method', str(ism.rank)))

		map = {
				ism.random	: self.select_random,
				ism.rank	: self.select_by_rank,
				ism.score	: self.select_by_score,
				ism.size	: self.select_by_size,
				ism.time	: self.select_by_time
				}

		self._select = map[method]


	def select(self):
		return self._select()


	def select_random(self):
		index = randint(0, self._images.length - 1)
		image = self._images.get_image(index)

		self._images.del_image(index)
		return image


	def select_by_rank(self, desc=True):
		image = self._images.get_image(fn=lambda l : min(l, key=lambda i: i.rank))
		self._images.del_image(image=image)

		return image


	def select_by_score(self, desc=True):
		pass


	def select_by_size(self, desc=False):
		pass


	def select_by_time(self, desc=False):
		pass


	def add_trace(self, msg, print_step=True):
		if self._trace is not None:
			self._trace.add_step('random %s'%self.image_alias, image.url or image.context_url, overwrite=True, print_step=print_step)
