from typing import Self


class StringBuilder:
	def __init__(self, *args):
		self.__text: list[str] = []
		self.__text.extend(map(str, args))

	def append(self, *args) -> Self:
		self.__text.extend(map(str, args))
		return self

	def append_join(self, sep:str, *args) -> Self:
		self.__text.extend(sep.join(map(str, args)))
		return self

	def append_line(self, *args) -> Self:
		self.__text.extend(map(str, args))
		self.__text.append("\n")
		return self

	def __str__(self):
		return ''.join(self.__text)
