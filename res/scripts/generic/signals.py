from typing import Callable

class Signal:
	def __init__(self):
		self.__funcs: list[Callable] = []

	def add_listener(self, func: Callable) -> None:

		self.__funcs.append(func)

	def remove_listener(self, func: Callable) -> None:
		try:
			self.__funcs.remove(func)
		except ValueError:
			pass

	def emit(self, *args, **kws) -> None:
		for func in self.__funcs:
			func(*args, **kws)

	def __iadd__(self, func: Callable):
		self.add_listener(func)
		return self

	def __isub__(self, func: Callable):
		self.remove_listener(func)
		return self
