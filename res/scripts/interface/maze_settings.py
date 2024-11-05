from res.scripts.Vectors import Vector2


class MazeSettings:
	def __init__(self):
		self.origin_color = "red"
		self.node_color = "black"
		self.arrow_color = "gray"
		self.arrow_just_created_color = "orange"
		self.path_arrow_color = "cadetblue3"
		self.path_nodes_color = "blue"
		self.node_spacing = 50
		self.node_radius = 5
		self.start_point = Vector2(20, 20)
