from typing import Callable, Set


class Signal:
	def __init__(self):
		self.__funcs: Set[Callable] = set()

	def add_listener(self, func: Callable) -> None:

		self.__funcs.add(func)

	def remove_listener(self, func: Callable) -> None:
		self.__funcs.discard(func)

	def emit(self, *args, **kws) -> None:
		for func in self.__funcs:
			func(*args, **kws)

	def __iadd__(self, func: Callable):
		self.add_listener(func)
		return self

	def __isub__(self, func: Callable):
		self.remove_listener(func)
		return self
