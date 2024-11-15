from res.scripts.generic.signals import Signal


class MazeSettings:
	def __init__(self):
		self.settings_changed = Signal()
		self.origin_color = "red"
		self.wall_color = "black"
		self.node_color = "black"
		self.edge_color = "gray"
		self.edge_just_created_color = "orange"
		self.path_edge_color = "cadetblue3"
		self.path_nodes_color = "blue"
		self.maze_size = 7, 7
		self.node_spacing = 50
		self.node_radius = 5

	def __setattr__(self, key, value):
		super().__setattr__(key, value)
		self.settings_changed.emit({key: value})
