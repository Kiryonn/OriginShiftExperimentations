import random

from res.scripts.data_only.constants import Position, Maze, Size
from res.scripts.data_only.utils import generate_default_maze, neighbors


def origin_shift(maze: Maze, origin: Position) -> Position:
	nodes = [n for n in neighbors(origin) if n in maze]
	new_origin = random.choice(nodes)
	maze[origin] = new_origin
	maze[new_origin] = None
	return new_origin


def generation_os(maze_size: Size, algo=origin_shift) -> tuple[Maze, Position]:
	maze, origin = generate_default_maze(maze_size)
	unvisited = set(maze)
	unvisited.discard(origin)
	threshold: int = int(maze_size[0] * maze_size[1] * 0.1)
	while len(unvisited) > threshold:
		origin = algo(maze, origin)
		unvisited.discard(origin)
	return maze, origin
