import random
from bisect import bisect
from itertools import accumulate

from res.scripts.data_only.constants import Size, Position, Maze
from res.scripts.data_only.utils import generate_default_maze, neighbors


def weighted_origin_shift(maze: Maze, origin: Position, visit_count: dict[Position, int]) -> Position:
	nodes = neighbors(origin, lambda e: e in maze)
	cum_weights = list(accumulate(1 / visit_count[n] for n in nodes))
	new_origin = nodes[bisect(cum_weights, random.random() * cum_weights[-1], 0, len(nodes))]
	maze[origin] = new_origin
	maze[new_origin] = None
	visit_count[new_origin] += 1
	return new_origin


def generation_wos(maze_size: Size, algo=weighted_origin_shift):
	maze, origin = generate_default_maze(maze_size)
	threshold = int(maze_size[0] * maze_size[1] * 0.1)
	visit_count = {k: 1 for k in maze}
	visit_count[origin] = 2
	remaining_unvisited = len(maze) - 1
	while remaining_unvisited > threshold:
		origin = algo(maze, origin, visit_count)
		if visit_count[origin] == 2:
			remaining_unvisited -= 1
	return maze, origin
