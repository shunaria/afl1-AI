from collections import deque


class Node:
	def __init__(self, state, parent=None):
		self.state = state
		self.parent = parent


class StackFrontier:
	def __init__(self):
		self.frontier = []

	def add(self, node):
		self.frontier.append(node)

	def remove(self):
		if self.empty():
			raise IndexError("Frontier kosong")
		return self.frontier.pop()

	def empty(self):
		return len(self.frontier) == 0

	def contains_state(self, state):
		return any(node.state == state for node in self.frontier)


class QueueFrontier(StackFrontier):
	def __init__(self):
		self.frontier = deque()

	def remove(self):
		if self.empty():
			raise IndexError("Frontier kosong")
		return self.frontier.popleft()


# Assumption: the two road columns in the image are parallel branches
# from Jalan Timor and merge at Jalan Haji Bau.
GRAPH = {
	"jalan irian": ["jalan timor"],
	"jalan timor": ["jalan irian", "jalan nusantara", "jalan sulawesi"],
	"jalan nusantara": ["jalan timor", "jalan ujung pandang"],
	"jalan ujung pandang": ["jalan nusantara", "jalan pattimura"],
	"jalan pattimura": ["jalan ujung pandang", "jalan somba opu"],
	"jalan somba opu": ["jalan pattimura", "jalan datumuseng"],
	"jalan datumuseng": ["jalan somba opu", "jalan lamadukelleng"],
	"jalan lamadukelleng": ["jalan datumuseng", "jalan haji bau"],
	"jalan sulawesi": ["jalan timor", "jalan riburane"],
	"jalan riburane": ["jalan sulawesi", "jalan ahmad yani"],
	"jalan ahmad yani": ["jalan riburane", "jalan kajaolalido"],
	"jalan kajaolalido": ["jalan ahmad yani", "jalan botolempangan"],
	"jalan botolempangan": ["jalan kajaolalido", "jalan arif rate"],
	"jalan arif rate": ["jalan botolempangan", "jalan haji bau"],
	"jalan haji bau": ["jalan arif rate", "jalan lamadukelleng", "jalan metro tanjung bunga"],
	"jalan metro tanjung bunga": ["jalan haji bau", "masuk ke CPI"],
	"masuk ke CPI": ["jalan metro tanjung bunga", "sampai UCM"],
	"sampai UCM": ["masuk ke CPI"],
}


def graph_search(start, goal, frontier):
	frontier.add(Node(start))
	explored = set()

	while not frontier.empty():
		node = frontier.remove()

		# Test the goal when it is removed, before expanding it.
		if node.state == goal:
			path = []
			while node is not None:
				path.append(node.state)
				node = node.parent
			return list(reversed(path)), explored

		explored.add(node.state)
		neighbors = sorted(GRAPH.get(node.state, []))

		# Reverse push order so a stack visits neighbors alphabetically.
		if isinstance(frontier, StackFrontier) and not isinstance(frontier, QueueFrontier):
			neighbors.reverse()

		for neighbor in neighbors:
			if neighbor not in explored and not frontier.contains_state(neighbor):
				frontier.add(Node(neighbor, node))

	return None, explored


if __name__ == "__main__":
	start = "jalan irian"
	goal = "sampai UCM"
	solution, explored = graph_search(start, goal, QueueFrontier())

	print("Jalur:", " -> ".join(solution) if solution else "Tidak ditemukan")
	print("Node diekspansi:", sorted(explored))
