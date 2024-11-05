import math
import networkx as nx
import random as rd
import tkinter as tk

from res.scripts.Vectors import Vector2, Vector2i
from res.scripts.interface.maze_settings import MazeSettings


class Maze(tk.Canvas):
	def __init__(self, master, size: Vector2i):
		size = Vector2i.max(Vector2i(3, 3), size)
		super(Maze, self).__init__(master)
		self.__graph: nx.DiGraph = nx.DiGraph()
		self.__origins: set[Vector2i] = set()
		self.__size: Vector2i = size
		self.__solution_extremities: tuple[Vector2i, Vector2i] = Vector2i(0, 0), Vector2i(0, 0)
		self.__solution: tuple[list[Vector2i], int] | None = [], 0
		self.__last_created_arrows: list[int] = []
		self.__is_solution_showned: bool = False
		self.settings: MazeSettings = MazeSettings()
		self.unvisited_nodes: set[Vector2i] = set()
		self.visit_count: dict[Vector2i, int] = {}
		self.redraw()

	def __is_solution_showned_getter(self) -> bool:
		return self.__is_solution_showned

	# noinspection PyTypeChecker
	is_solution_showned = property(__is_solution_showned_getter)

	def redraw(self) -> None:
		self.delete('all')
		self.__graph.clear()
		self.__origins.clear()
		self.unvisited_nodes.clear()
		last_col = self.__size.y - 1
		for row in range(self.__size.x):
			for col in range(self.__size.y):
				position = Vector2i(row, col)
				self.unvisited_nodes.add(position)
				self.add_node(position)
				if col > 0:
					self.add_edge(position - Vector2i(0, 1), position)
					if col == last_col and row > 0:
						self.add_edge(position - Vector2i(1, 0), position)
		origin = Vector2i(self.__size.x - 1, self.__size.y - 1)
		self.add_origin(origin)
		self.visit_count = {n: 0 for n in self.unvisited_nodes}
		self.visit_count[origin] += 1
		self.unvisited_nodes.discard(origin)
		self.change_solution_node(Vector2i(self.__size.x - 1, 0))
		self.change_solution_node(Vector2i(0, self.__size.y - 1))

	def __get_solution_arrows(self) -> list[int]:
		solution, sep = self.__solution
		arrows: list[int] = []
		for i in range(1, len(solution)):
			node1, node2 = solution[i - 1], solution[i]
			if i >= sep:
				node1, node2 = node2, node1
			if self.__graph.has_edge(node1, node2):
				arrows.append(self.__get_graphical_arrow(node1, node2))
		return arrows

	def show_solution(self):
		self.__solution = self.recalculate_solution()
		self.__is_solution_showned = True
		color = self.settings.path_arrow_color
		for arrow in self.__get_solution_arrows():
			self.__recolor_arrow(arrow, color)

	def hide_solution(self):
		color = self.settings.arrow_color
		self.__is_solution_showned = False
		for arrow in self.__get_solution_arrows():
			self.__recolor_arrow(arrow, color)

	def recalculate_solution(self) -> tuple[list[Vector2i], int]:
		start, end = self.__solution_extremities
		path1: list[Vector2i] = [start]
		path2: list[Vector2i] = [end]
		# calc path from start to origin
		while start not in self.__origins:
			start = self.__graph.neighbors(start).__next__()
			path1.append(start)
		# calc path (end -> origin) until intersection of path (start -> origin) found
		while end not in path1:
			end = self.__graph.neighbors(end).__next__()
			path2.append(end)
		# cut excess nodes visited on path (start -> origin)
		while path1[-1] != end:
			path1.pop()
		# remove duplicate intersection point
		path2.pop()
		# the solution is the (start -> intersection) + (end -> intersection) reversed
		return path1 + path2[::-1], len(path1)

	def add_origin(self, position: Vector2i) -> None:
		self.__origins.add(position)
		self.__recolor_node(self.__get_graphical_node(position), self.settings.origin_color)
		for connexion in list(self.__graph.neighbors(position)):
			self.remove_edge(position, connexion)

	def remove_origin(self, position: Vector2i) -> None:
		color = self.settings.path_nodes_color if position in self.__solution_extremities else self.settings.node_color
		self.__recolor_node(self.__get_graphical_node(position), color)
		self.__origins.discard(position)

	def toggle_origin(self, o: Vector2i) -> None:
		if o in self.__origins:
			self.remove_origin(o)
			self.add_edge(o, rd.choice(self.adjacent_nodes(o)))
		else:
			self.add_origin(o)

	def change_solution_node(self, position: Vector2i) -> None:
		# recolor old start
		old_start = self.__solution_extremities[0]
		if self.__graph.has_node(old_start):
			self.__recolor_node(self.__get_graphical_node(old_start), self.settings.node_color)
		# recolor new end
		if self.__graph.has_node(position):
			self.__recolor_node(self.__get_graphical_node(position), self.settings.path_nodes_color)
		# update solution start/end
		self.__solution_extremities = self.__solution_extremities[1], position

	def add_edge(self, p1: Vector2i, p2: Vector2i) -> None:
		start: Vector2 = self.settings.start_point + p1.swap() * self.settings.node_spacing
		end: Vector2 = self.settings.start_point + p2.swap() * self.settings.node_spacing
		direction: Vector2 = (end - start).normalized
		offset: Vector2 = direction * self.settings.node_radius
		start += offset
		end -= offset

		arrow = self.create_line(*start, *end, arrow=tk.LAST, fill=self.settings.arrow_just_created_color)
		self.__graph.add_edge(p1, p2, gfarrow=arrow)
		self.__last_created_arrows.append(arrow)

	def remove_edge(self, p1: Vector2i, p2: Vector2i) -> None:
		if not self.__graph.has_edge(p1, p2):
			return
		self.delete(self.__get_graphical_arrow(p1, p2))
		self.__graph.remove_edge(p1, p2)

	def add_node(self, position: Vector2i) -> None:
		middle = self.settings.node_spacing * Vector2i(position.y, position.x) + self.settings.start_point
		radius_vector = self.settings.node_radius * Vector2(1, 1)
		start = middle - radius_vector
		end = middle + radius_vector
		color = self.settings.path_nodes_color if position in self.__solution_extremities else self.settings.node_color

		node = self.create_oval(*start, *end, fill=color, outline='')
		self.tag_bind(node, '<Button-3>', lambda e, p=position: self.toggle_origin(p))
		self.tag_bind(node, '<Button-1>', lambda e, p=position: self.change_solution_node(p))
		self.__graph.add_node(position, gfnode=node)

	def remove_node(self, position: Vector2i) -> None:
		if not self.__graph.has_node(position):
			return
		successors = list(self.__graph.neighbors(position))
		for connexion in successors:
			self.remove_edge(position, connexion)
		predecessors = list(self.__graph.predecessors(position))
		for connexion in predecessors:
			self.remove_edge(connexion, position)
		self.delete(self.__get_graphical_node(position))
		self.__graph.remove_node(position)
		self.__origins.discard(position)

	def resize(self, size: Vector2i) -> None:
		self.__size = size
		self.redraw()

	def step(self) -> None:
		while self.__last_created_arrows:
			arrow = self.__last_created_arrows.pop()
			self.__recolor_arrow(arrow, self.settings.arrow_color)
		new_origins: set[Vector2i] = set()
		while self.__origins:
			origin = self.__origins.pop()
			directions, weigths = self.get_weigthed_directions(origin)
			new_origin = rd.choices(directions, weights=weigths, k=1)[0]

			self.add_edge(origin, new_origin)
			self.remove_origin(origin)
			new_origins.add(new_origin)
		for new_origin in new_origins:
			self.add_origin(new_origin)

	def get_weigthed_directions(self, position: Vector2i):
		directions: list[Vector2i] = self.adjacent_nodes(position)
		weigths = [1 / (self.visit_count[n] + 1) for n in directions]
		return directions, weigths

	def adjacent_nodes(self, node: Vector2i) -> list[Vector2i]:
		res: list[Vector2i] = []
		if 0 <= node.x - 1 < self.__size.x:
			res.append(Vector2i(node.x - 1, node.y))
		if 0 <= node.x + 1 < self.__size.x:
			res.append(Vector2i(node.x + 1, node.y))
		if 0 <= node.y - 1 < self.__size.y:
			res.append(Vector2i(node.x, node.y - 1))
		if 0 <= node.y + 1 < self.__size.y:
			res.append(Vector2i(node.x, node.y + 1))
		return res

	def __get_graphical_node(self, position: Vector2i) -> int:
		return self.__graph.nodes[position]['gfnode']

	def __get_graphical_arrow(self, p1: Vector2i, p2: Vector2i) -> int:
		return self.__graph.edges[p1, p2]['gfarrow']

	def __recolor_arrow(self, arrow: int, color: str) -> None:
		self.itemconfigure(arrow, fill=color)

	def __recolor_node(self, node: int, color: str) -> None:
		self.itemconfigure(node, fill=color)

	def get_area(self) -> tuple[int, int, int, int]:
		"""
		:return: [x, y, width, height]
		"""
		width, height = self.settings.node_spacing * (self.__size - Vector2i(1, 1)) + self.settings.start_point * 2
		return 0, 0, math.ceil(width), math.ceil(height)
