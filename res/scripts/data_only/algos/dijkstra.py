import heapq

from res.scripts.data_only.constants import Position, Maze
from res.scripts.data_only.utils import neighbors


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
