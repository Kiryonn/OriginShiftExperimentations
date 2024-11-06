import tkinter as tk
from typing import Any

from res.scripts.utils import isint, isfloat


class Spinbox(tk.Spinbox):
	def __init__(self, master: tk.Misc = None, cnf: dict[str, Any] = None, **kws):
		if cnf is None:
			cnf = {}
		super().__init__(master, cnf, **kws)
		self["validate"] = "all"
		self["validatecommand"] = self.register(self.__vcmd__), '%P'

	def __vcmd__(self, new_text) -> bool:
		if isint(new_text) or isfloat(new_text):
			return True
		if new_text == "":
			self.__set(0)
		return False

	def set(self, value):
		if isinstance(value, int | float):
			self.__set(value)
		if isinstance(value, str) and (isint(value) or isfloat(value)):
			self.__set(float(value))

	def get(self) -> str:
		return super().get()

	def __set(self, value):
		self.delete(0, "end")
		if self["from"] == self["to"]:
			self.insert(0, str(value).rstrip('0').rstrip('.'))
		else:
			if value > self["to"]:
				value = self["to"]
			elif value < self["from"]:
				value = self["from"]
			self.insert(0, str(value).rstrip('0').rstrip('.'))