from typing import Callable


class Signal:
	def __init__(self):
		self.__funcs = set()

	def add_listener(self, func: Callable):
		self.__funcs.add(func)

	def remove_listener(self, func: Callable):
		self.__funcs.discard(func)

	def emit(self, *args, **kws):
		for func in self.__funcs:
			func(*args, **kws)

	def __iadd__(self, func: Callable):
		self.add_listener(func)
		return self

	def __isub__(self, func: Callable):
		self.remove_listener(func)
		return self
