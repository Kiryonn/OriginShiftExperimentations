from datetime import datetime
import os
import tkinter as tk

from PIL import Image

from res.scripts.Vectors import Vector2i
from res.scripts.interface.constants import BASE_MAZE_SIZE, SCREENSHOTS_PATH
from res.scripts.interface.control_pannel import ControlPanel
from res.scripts.interface.maze import Maze

class Interface(tk.Tk):
	def __init__(self):
		super(Interface, self).__init__()

		self.maze = Maze(self, BASE_MAZE_SIZE)
		self.control_pannel = ControlPanel(self)

		self.control_pannel.place(x=0, y=0, relwidth=1, height=50)
		self.maze.place(x=0, y=50, relwidth=1, relheight=1)

		self.config(width=512, height=512)

		self.bind("<Button-1>", self.focus_fix)
		self.last_focused = self

		self.control_pannel.on_path_toggled += self.on_solution_button_clicked
		self.control_pannel.on_step_clicked += self.on_step_button_clicked
		self.control_pannel.on_maze_size_changed += self.on_maze_size_changed
		self.control_pannel.on_save_image_button_pressed += self.make_maze_screenshot

	def focus_fix(self, _event) -> None:
		x, y = self.winfo_pointerxy()
		widget = self.winfo_containing(x, y)
		if widget != self.last_focused:
			widget.focus()
			# if failed, ex clicked on canvas
			if self.focus_get() == self.last_focused:
				self.focus()
				self.last_focused = self
			else:
				self.last_focused = widget

	def on_solution_button_clicked(self, is_toggled: bool) -> None:
		if is_toggled:
			self.maze.show_solution()
		else:
			self.maze.hide_solution()

	def on_step_button_clicked(self, nb_steps: int) -> None:
		for _ in range(nb_steps):
			self.maze.step()
		if self.maze.is_solution_showned:
			self.maze.hide_solution()
			self.maze.show_solution()

	def on_maze_size_changed(self, size: Vector2i) -> None:
		self.maze.resize(size)

	def get_color(self, color) -> tuple[int, ...]:
		return tuple(c // 256 for c in self.winfo_rgb(color))

	def make_maze_screenshot(self):
		area = self.maze.get_area()
		w, h = area[2], area[3]
		im = Image.new("RGB", (w, h))
		colors = {}

		maze_bg_color = self.get_color(self.maze.cget("bg"))
		for x in range(w):
			for y in range(h):
				obj = self.maze.find_overlapping(x, y, x, y)
				color = maze_bg_color if len(obj) == 0 else self.get_color(self.maze.itemcget(obj[0], "fill"))
				if color in colors:
					colors[color] += 1
				else:
					colors[color] = 0
				im.putpixel((x, y), color)
		if not os.path.exists(SCREENSHOTS_PATH):
			os.makedirs(SCREENSHOTS_PATH)
		filename = SCREENSHOTS_PATH + datetime.now().strftime("%Y_%m_%d-%H_%M_%S") + ".png"
		im.save(filename, format="png")
		print("image saved successfully at", os.path.abspath(filename))


if __name__ == '__main__':
	app = Interface()
	app.mainloop()
