def bellman_ford(G, source):
    """Return the shortest paths from source to all other nodes in G."""
    d = dict(zip(G.keys(), [0] + [len(G) + 1] * (len(G) - 1)))
    d[source] = 0

    for node in G:
	    for neighbor in G[node]:
		    d[neighbor] = min(d[neighbor], d[node] + 1)
		    d[node] = min(d[node], d[neighbor] + 1)

    return ''.join([c + ':' + str(i) + ' ' 
	                for (c, i) in zip(d.keys(), d.values())])

def main():

    G = {'a': ['b','c'],
         'b': ['a','c','d','h'],
         'c': ['a','b','d'],
         'd': ['b','c','e'],
         'e': ['d','f','g'],
         'f': ['e','h'],
         'g': ['e'],
         'h': ['i'],
         'i': ['h']}

    print bellman_ford(G, source='a')

if __name__ == '__main__':
	main()