# Construct a spanning tree using spanning tree protocol
import numpy as np

def spanning_tree(G):
    """Input: A graph g.
       Output: A spanning tree of graph g."""
    n = len(G)
    T = np.array([[0 for i in range(n)] for j in range(n)])
    # msg format: [self, dist, root]
    msg = [[i, 0, i] for i in range(n)]
    for i in range(n):
        dist = 1
        for j in range(i + 1, n):
            if G[i][j] == 1:
                if msg[i][2] < msg[j][2]:
                    msg[j] = [j, dist, i]
                    T[i][j] = 1
                    T[j][i] = 1
            dist += 1
    return T

def main():
    # insert code here
    G = [[0,1,1,0,0],
         [1,0,1,0,1],
         [1,1,0,1,1],
         [0,0,1,0,1],
         [0,1,1,1,0]]
    T = spanning_tree(G)
    print T

if __name__ == '__main__':
    main()