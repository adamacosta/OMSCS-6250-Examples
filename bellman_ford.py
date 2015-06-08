"""
Implements the Bellman-Ford algorithm, as described at 
http://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm.
This algorithm is used in the distance-vector protocol for 
finding paths between routers in a computer network.
"""


class Graph:
	"""Purpose-specific.

	This is only for demonstration and not a general-purpose graph.
	"""
	def __init__(self, nodes, edges):
		self.nodes = nodes
		self.edges = edges

	def bellman_ford(self, source):
		# Sum of all edges + 1 serves as 'infinity'
		distance = dict(zip(self.nodes, 
			               [sum(self.edges.values()) + 1] * len(self.nodes)))
		distance[source] = 0
		print distance
		for node in self.nodes:
			for edge in self.edges:
				if distance[edge[0]] + self.edges[edge] < distance[edge[1]]:
					distance[edge[1]] = distance[edge[0]] + self.edges[edge] 
			print distance


if __name__ == '__main__':
	edges = ['ab', 'ac', 'bc', 'bd', 'bh', 'cd', 'de', 'ef', 'eg', 'fh', 'hi']
	weights = [1, 3, 2, 6, 1, 5, 4, 2, 2, 5, 4]
	G = Graph(set(''.join(edges)), dict(zip(edges, weights)))
	G.bellman_ford(source='a')