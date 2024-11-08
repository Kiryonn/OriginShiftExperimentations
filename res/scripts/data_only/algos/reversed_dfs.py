import random

from res.scripts.data_only.constants import Position, Maze, Size
from res.scripts.data_only.utils import neighbors


def reversed_dfs(size: Size) -> tuple[Maze, Position]:
	# initialize needed data
	maze: Maze = {}
	unvisited = set((i, j) for i in range(size[0]) for j in range(size[1]))
	stack: list[Position] = []
	origin = random.randrange(size[0]), random.randrange(size[1])

	# update data
	maze[origin] = None
	stack.append(origin)
	unvisited.discard(origin)
	current_node: Position

	# Apply reversed DFS
	while stack:
		current_node = stack[-1]
		ns = neighbors(current_node, lambda e: e in unvisited)
		# backtrack
		if not ns:
			stack.pop()
			continue
		chosen = ns[random.randrange(0, len(ns))]
		stack.append(chosen)
		unvisited.discard(chosen)
		maze[chosen] = current_node
	return maze, origin
