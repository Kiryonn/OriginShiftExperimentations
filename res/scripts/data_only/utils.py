from typing import Callable
from res.scripts.data_only.constants import Size, Position, Maze


units = ["s", "ms", "μs", "ns"]


def generate_default_maze(size: Size) -> tuple[Maze, Position]:
	rows, cols = size
	maxrow, maxcol = rows - 1, cols - 1
	maze: Maze = {(i, j): (i + 1, j) if j == maxcol else (i, j + 1) for i in range(rows) for j in range(cols)}
	maze[maxrow, maxcol] = None
	return maze, (maxrow, maxcol)


def neighbors(node: Position, predicate: Callable[[Position], bool] = None) -> list[Position]:
	row, col = node
	res = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
	return res if predicate is None else [n for n in res if predicate(n)]


def print_stats(number_list, indents=0):
	if not number_list:
		return
	sorted_list = sorted(number_list)
	cumulated_sum = sum(sorted_list)
	indentation = '\t' * indents
	print(indentation + 'min    :', sorted_list[0])
	print(indentation + 'max    :', sorted_list[-1])
	print(indentation + 'average:', cumulated_sum / len(sorted_list))
	print(indentation + 'Q1     :', sorted_list[len(sorted_list) // 4])
	print(indentation + 'Q3     :', sorted_list[len(sorted_list) * 3 // 4])


def maze_to_string(maze: Maze, size: Size) -> str:
	rows = [['+' if not i % 2 and not j % 2 else ' ' for j in range(size[1] * 2 - 1)] for i in range(size[0] * 2 - 1)]
	for n1 in maze:
		i, j = n1
		n2 = maze[n1]
		if n2 is None: continue
		elif n1[0] < n2[0]: rows[i * 2 + 1][j * 2] = '|'
		elif n2[0] < n1[0]: rows[i * 2 - 1][j * 2] = '|'
		elif n1[1] < n2[1]: rows[i * 2][j * 2 + 1] = '-'
		elif n2[1] < n1[1]: rows[i * 2][j * 2 - 1] = '-'
	return '\n'.join(''.join(row) for row in rows)
