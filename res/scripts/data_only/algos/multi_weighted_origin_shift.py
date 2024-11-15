import random
from bisect import bisect

from res.scripts.data_only.constants import Size, Position, Maze
from res.scripts.data_only.utils import neighbors


def multi_weighted_origins_shift(maze: Maze, origins: set[Position], visit_count: dict[Position, int]) -> set[Position]:
	new_origins: set[Position] = set()
	new_origin: Position
	for o in origins:
		nodes = [n for n in neighbors(o) if n in maze]
		cumulated_weights = []
		total = 0
		n = len(nodes)
		for i in range(n):
			total += 1 / visit_count[nodes[i]]
			cumulated_weights.append(total)
		new_origin = nodes[bisect(cumulated_weights, random.random() * total, 0, n)]
		maze[o] = new_origin
		new_origins.add(new_origin)
		visit_count[new_origin] += 1
	for o in new_origins:
		maze[o] = None
	return new_origins


# noinspection SpellCheckingInspection
def generation_mwos(maze_size: Size, algo=multi_weighted_origins_shift) -> tuple[Maze, Position]:
	max_j = maze_size[1] - 1
	maze: Maze = {}
	origins: set[Position] = set()
	visit_count: dict[Position, int] = {}
	for i in range(maze_size[0]):
		for j in range(maze_size[1]):
			node: Position = i, j
			if i & 1 == j & 1:
				maze[node] = None
				origins.add(node)
				visit_count[node] = 2
			elif j == max_j:
				maze[node] = i, j - 1
				visit_count[node] = 1
			else:
				maze[node] = i, j + 1
				visit_count[node] = 1
	while len(origins) > 1:
		origins = algo(maze, origins, visit_count)
	return maze, origins.pop()
