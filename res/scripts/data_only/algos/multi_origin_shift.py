import random

from res.scripts.data_only.constants import Size, Position, Maze
from res.scripts.data_only.utils import neighbors


def __process_origin(maze: Maze, origin: Position) -> Position:
	new_origin = random.choice([n for n in neighbors(origin) if n in maze])
	maze[origin] = new_origin
	return new_origin

def multi_origins_shift(maze: Maze, origins: set[Position]) -> set[Position]:
	origins = {__process_origin(maze, o) for o in origins}
	for o in origins: maze[o] = None
	return origins

def generation_mos(maze_size: Size, algo=multi_origins_shift):
	max_j = maze_size[1] - 1
	maze = {(i, j): None if i & 1 == j & 1 else (i, j + 1) if j != max_j else (i, j - 1) for i in range(maze_size[0]) for j in range(maze_size[1])}
	origins = {n for n in maze if maze[n] is None}
	while len(origins) > 1: origins = algo(maze, origins)
	return maze, origins
