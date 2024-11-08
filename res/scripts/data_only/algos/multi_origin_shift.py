import random

from res.scripts.data_only.constants import Size, Position, Maze
from res.scripts.data_only.utils import neighbors


def multi_origins_shift(maze: Maze, origins: set[Position]) -> set[Position]:
	new_origins = set()
	for origin in origins:
		new_origin = random.choice(neighbors(origin, lambda e: e in maze))
		new_origins.add(new_origin)
		maze[origin] = new_origin
	# separated to avoid bugs
	for origin in new_origins:
		maze[origin] = None
	return new_origins


def generation_mos(maze_size: Size, algo=multi_origins_shift):
	maze = {(i, j): None for i in range(maze_size[0]) for j in range(maze_size[1])}
	origins = set(maze.keys())
	while len(origins) > 2:
		origins = algo(maze, origins)
	return maze, origins
