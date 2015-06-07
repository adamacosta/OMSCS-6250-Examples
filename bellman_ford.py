"""
Implements the Bellman-Ford algorithm, as described at 
http://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm.
This algorithm is used in the distance-vector protocol for 
finding paths between routers in a computer network.
"""

class Graph:
	"""
	class Graph
	
	params
	------
	nodes: a list of names for nodes in the graph 
	edges: a list of lists of the form [u, v, w] where w is the weight.
	"""
	def __init__(self, nodes, edges):
		assert(len(nodes) > 1)
		assert(len(edges) > 1)
		self.nodes = nodes
		self.edges = edges

	def bellman_ford(self, source):
		distance = {}
		predecessor = {}
		for node in self.nodes:
			distance[node] = 10 ** 100
			predecessor[node] = None
		distance[source] = 0
		for node in self.nodes:
			for edge in self.edges:
				if distance[edge[0]] + edge[2] < distance[edge[1]]:
					distance[edge[1]] = distance[edge[0]] + edge[2]
					predecessor[edge[1]] = edge[0]
		return distance, predecessor

if __name__ == '__main__':
	V = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
	E = [['a','b', 1], ['a','c', 3], ['b','c', 2],
	     ['b','d', 6], ['b','h', 1], ['c','d', 5],
	     ['d','e', 4], ['e','f', 2], ['e','g', 2],
	     ['f','h', 5], ['h','i', 4]]
	G = Graph(V, E)
	print G.bellman_ford(source='a')