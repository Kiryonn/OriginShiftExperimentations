import tkinter as tk
from typing import Type

from ..generic.singleton import Singleton
from .data.maze_settings import MazeSettings
from .settings import Settings


class Interface(tk.Tk, metaclass=Singleton):
	def __init__(self):
		super(Interface, self).__init__()
		self.title("Maze Testing Interface")
		self.settings = Settings(self)
		self.maze_settings = MazeSettings()
		self.maze_settings.maze_size = 8, 8
		self.__current_scene: tk.Widget = None

	def change_scene(self, scene: Type[tk.Widget], *args, **kws):
		new_scene = scene(self, *args, **kws)
		if self.__current_scene is not None:
			self.__current_scene.place_forget()
		new_scene.place(x=0, y=0, relwidth=1, relheight=1)
		if self.__current_scene is not None:
			self.__current_scene.destroy()
		self.__current_scene = new_scene
