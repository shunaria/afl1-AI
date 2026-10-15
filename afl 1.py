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


GRAPH = {
	"Denpasar": ["Kuta", "Mengwi", "Ngerebong"],
	"Kuta": ["Denpasar"],
	"Mengwi": ["Denpasar", "Ubud"],
	"Ngerebong": ["Denpasar", "Sukawati", "Ubud"],
	"Sukawati": ["Ngerebong", "Padangbai"],
	"Ubud": ["Mengwi", "Ngerebong", "Padangbai"],
	"Padangbai": ["Sukawati", "Ubud"],
}


def graph_search(start, goal, frontier):
	frontier.add(Node(start))
	explored = set()

	while not frontier.empty():
		node = frontier.remove()

		# Goal diuji saat node dikeluarkan dari frontier, sebelum diekspansi.
		if node.state == goal:
			path = []
			while node is not None:
				path.append(node.state)
				node = node.parent
			return list(reversed(path)), explored

		explored.add(node.state)

		neighbors = sorted(GRAPH.get(node.state, []))
		if isinstance(frontier, StackFrontier) and not isinstance(frontier, QueueFrontier):
			neighbors.reverse()

		for neighbor in neighbors:
			if neighbor not in explored and not frontier.contains_state(neighbor):
				frontier.add(Node(neighbor, node))

	return None, explored


if __name__ == "__main__":
	solution, explored = graph_search(
		"Denpasar",
		"Padangbai",
		QueueFrontier(),
	)
	print("Jalur:", " -> ".join(solution) if solution else "Tidak ditemukan")
	print("Node diekspansi:", sorted(explored))
