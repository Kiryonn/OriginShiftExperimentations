import random
import time
import timeit
import heapq
from bisect import bisect
from itertools import accumulate
from typing import Callable

Position = tuple[int, int]
Size = tuple[int, int]
Maze = dict[Position, Position | None]


def generate_default_maze(size: Size) -> Maze:
	rows, cols = size
	maxrow, maxcol = rows - 1, cols - 1
	maze: Maze = {}
	for row in range(rows):
		for col in range(cols):
			# right most nodes points downwards
			if col == maxcol:
				maze[row, col] = row + 1, col
			# other nodes points right
			else:
				maze[row, col] = row, col + 1
	#  origin node points nowhere
	maze[maxrow, maxcol] = None
	return maze


def neighbors(node: Position, predicate: Callable[[Position], bool]=None) -> list[Position]:
	row, col = node
	res = [(row-1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
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

def print_results(title: str, *args: tuple[str, list]):
	print(title)
	for label, data in args:
		print(label)
		print_stats(data, indents=1)
		print()

# region origin_shift
def origin_shift(maze: Maze, origin: Position) -> Position:
	nodes = neighbors(origin, lambda e: e in maze)
	new_origin = random.choice(nodes)
	maze[origin] = new_origin
	maze[new_origin] = None
	return new_origin


def test_origin_shift(maze_size: Size, nb_tests: int):
	maze = generate_default_maze(maze_size)
	origin = maze_size[0] - 1, maze_size[1] - 1
	nb_calls: list[int] = []
	os_durations: list[float] = []
	durations: list[float] = []
	threshold: int = int(maze_size[0] * maze_size[1] * 0.1)
	for _ in range(nb_tests):
		# test setup
		unvisited = set(maze)
		unvisited.discard(origin)
		nb_calls.append(0)
		durations.append(0)
		# loop
		while len(unvisited) > threshold:
			# real test
			start_time = time.time()
			origin = origin_shift(maze, origin)
			end_time = time.time()

			# update test data
			unvisited.discard(origin)
			nb_calls[-1] += 1
			time_taken_ms = (end_time - start_time) * 1000
			durations[-1] += time_taken_ms
			os_durations.append(time_taken_ms * 1000)
	print_results(
		f"Maze of size {maze_size[0]} by {maze_size[1]} over {nb_tests} iterations",
		("Nb Calls", nb_calls),
		("Maze Generation Duration (in ms)", durations),
		("Algorithm Execution Time (in ns)", os_durations)
	)


# endregion origin_shift


# region solving
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


def dijkstra(maze: Maze, _from: Position, to: Position) -> list[Position]:
	# almost entirely copied pasted from
	# https://www.askpython.com/python/examples/dijkstras-algorithm-python

	# Initialize distances dictionary
	distances = {node: float('inf') for node in maze}
	distances[_from] = 0

	# Initialize priority queue
	pq = [(0, _from)]
	# Initialize previous node dictionary to store shortest path
	previous = {}
	while pq:
		current_distance, current_node = heapq.heappop(pq)
		# If we already found a shorter path, skip
		if current_distance > distances[current_node]:
			continue
		# Stop if we reached the destination
		if current_node == to:
			break
		# Explore neighbors
		for neighbor in neighbors(current_node, lambda e: e in maze):
			# if the path between the 2 nodes doesn't exist, ignore it
			if maze[current_node] != neighbor and maze[neighbor] != current_node:
				continue
			new_distance = current_distance + 1
			if new_distance < distances[neighbor]:
				distances[neighbor] = new_distance
				heapq.heappush(pq, (new_distance, neighbor))
				previous[neighbor] = current_node

	# Reconstruct the shortest pathx
	path = []
	node = to
	while node != _from:
		path.append(node)
		node = previous[node]
	path.append(_from)
	path.reverse()

	return path


def test_solving(maze_size: Size, nb_tests: int):
	nb_nodes = maze_size[0] * maze_size[1]
	_from = maze_size[0] - 1, 0
	to = 0, maze_size[1] - 1
	maze = generate_default_maze(maze_size)
	origin = maze_size[0] - 1, maze_size[1] - 1
	dijkstra_durations = []
	direct_pathing_durations = []

	for _ in range(nb_tests):
		# change the maze with origin shift
		for _ in range(nb_nodes * 10):
			origin = origin_shift(maze, origin)

		# test both solving methods
		direct_duration = timeit.timeit(lambda: direct_pathing(maze, _from, to), number=1)
		dijkstra_duration = timeit.timeit(lambda: dijkstra(maze, _from, to), number=1)

		# save timings
		dijkstra_durations.append(dijkstra_duration * 1_000_000)
		direct_pathing_durations.append(direct_duration * 1_000_000)
	print_results(
		f"Solving maze of size {maze_size[0]} by {maze_size[1]} over {nb_tests} iterations",
		("Dijkstra (ns)", dijkstra_durations),
		("Direct Pathing (ns)", direct_pathing_durations)
	)

# endregion solving


# region weighted_origin_shift
def weighted_origin_shift(maze: Maze, origin: Position, visit_count: dict[Position, int]) -> Position:
	nodes = neighbors(origin, lambda e: e in maze)
	weights = [1 / visit_count[n] for n in nodes]
	cum_weights = list(accumulate(weights))
	new_origin = nodes[bisect(cum_weights, random.random() * cum_weights[-1], 0, len(weights))]
	maze[origin] = new_origin
	maze[new_origin] = None
	visit_count[new_origin] += 1
	return new_origin


def test_weighted_origin_shift(maze_size: Size, nb_tests: int):
	maze = generate_default_maze(maze_size)
	origin = maze_size[0] - 1, maze_size[1] - 1
	threshold = int(maze_size[0] * maze_size[1] * 0.1)
	nb_calls: list[int] = []
	durations: list[float] = []
	wos_durations: list[float] = []
	for _ in range(nb_tests):
		# test setup
		nb_calls.append(0)
		durations.append(0)
		visit_count: dict[Position, int] = {k: 1 for k in maze.keys()}
		visit_count[origin] = 2
		remaining_unvisited = len(maze) - 1
		# loop
		while remaining_unvisited > threshold:
			# real test
			start_time = time.time()
			origin = weighted_origin_shift(maze, origin, visit_count)
			end_time = time.time()
			# update test data
			if visit_count[origin] == 2:
				remaining_unvisited -= 1
			nb_calls[-1] += 1
			time_taken_ms = (end_time - start_time) * 1000
			durations[-1] += time_taken_ms
			wos_durations.append(time_taken_ms * 1000)
	print_results(
		f"Maze of size {maze_size[0]} by {maze_size[1]} over {nb_tests} iterations",
		("Nb Calls", nb_calls),
		("Maze Generation Duration (in ms)", durations),
		("Algorithm Execution Time (in ns)", wos_durations)
	)

# endregion weighted_origin_shift


# region multi_origin_shift
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


def test_multi_origins(maze_size: Size, origins: set[Position], nb_iter: int):
	maze = generate_default_maze(maze_size)
	origins_translations: list[set[Position]] = [origins]
	for _ in range(nb_iter):
		origins = multi_origins_shift(maze, origins)
		origins_translations.append(origins)
	print(origins_translations)


# endregion multi_origin_shift

# region reversed_dfs
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
	currentNode = origin

	# Apply reversed DFS
	while (stack):
		currentNode = stack[-1]
		ns = neighbors(currentNode, lambda e: e in unvisited)
		# backtrack
		if not ns:
			stack.pop()
			continue
		choosen = ns[random.randrange(len(ns))]
		stack.append(choosen)
		unvisited.discard(choosen)
		maze[choosen] = currentNode
	return (maze, origin)


def test_reversed_dfs(maze_size: Size, nb_tests: int):
	durations = []
	for _ in range(nb_tests):
		start_time = time.time()
		reversed_dfs(maze_size)
		end_time = time.time()
		durations.append((end_time - start_time) * 1000)
	print_results(
		f"Maze of size {maze_size[0]} by {maze_size[1]} over {nb_tests} iterations",
		("Maze Generation Duration (in ms)", durations)
	)
# endregion reversed_dfs

if __name__ == '__main__':
	test_reversed_dfs((64, 64), 5000)
