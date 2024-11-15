import json
import os
import tkinter as tk
from tkinter import ttk

from res.scripts.generic.signals import Signal


class Settings:
	SETTINGS_PATH = "res/data/setttings.json"
	def __init__(self, master):
		self.on_theme_changed = Signal[str]()
		self.master = master
		self.__themeVar = tk.StringVar()
		self.__toplevel: tk.Toplevel = None

		self.__themeVar.trace_add("write", self.__on_theme_changed)

	def __on_theme_changed(self, *_):
		style = ttk.Style()
		new_theme = self.__themeVar.get()
		if new_theme == style.theme_use():
			return
		style.theme_use(new_theme)
		self.save()
		self.on_theme_changed.emit(new_theme)

	def load(self):
		with open(self.SETTINGS_PATH, 'r', encoding='utf-8') as file:
			settings = json.load(file)
		self.__themeVar.set(settings['theme'])

	def save(self):
		data = {
			"theme": self.__themeVar.get()
		}
		if not os.path.exists(self.SETTINGS_PATH):
			os.makedirs(self.SETTINGS_PATH, exist_ok=True)
		with open(self.SETTINGS_PATH, 'w', encoding='utf-8') as file:
			json.dump(data, file)

	def open(self):
		if self.__toplevel is not None:
			return
		self.__toplevel = tk.Toplevel(self.master)
		self.__toplevel.title("Settings")

	def close(self):
		if self.__toplevel is not None:
			self.__toplevel.destroy()

	def toggle(self):
		if self.__toplevel is not None:
			self.open()
		else:
			self.close()
