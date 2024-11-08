from res.scripts.data_only.constants import Position, Maze


def direct_pathing(maze: Maze, _from: Position, to: Position) -> list[Position]:
	if _from == to:
		return []

	path1: list[Position] = []
	path2: list[Position] = []

	while _from is not None:
		path1.append(_from)
		_from = maze[_from]

	while to is not None:
		path2.append(to)
		to = maze[to]

	intersection = path1[-1]
	while intersection == path2[-1]:
		intersection = path1[-1]
		path1.pop()
		path2.pop()

	path2.reverse()
	path1.append(intersection)
	path1.extend(path2)
	return path1
