import heapq
from Utils.utils import read_data, distance

iPair = tuple
 
# This class represents a directed graph using adjacency list representation
class Graph:
    def __init__(self, V: int): # Constructor
        self.V = V
        self.adj = [[] for _ in range(V)]
 
    def addEdge(self, u: int, v: int, w: int):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))
 
    # Prints shortest paths from s to t
    def shortestPath(self, s: int, t):
        # Create a priority queue to store vertices that are being preprocessed
        pq = []
        heapq.heappush(pq, (0, s))
 
        # Create a vector for distances and initialize all distances as infinite (INF)
        dist = [float('inf')] * self.V
        trace = [-1] * self.V
        dist[s] = 0
 
        while pq:
            d, u = heapq.heappop(pq)
            if u == t:
                break
 
            # 'i' is used to get all adjacent vertices of a vertex
            for v, weight in self.adj[u]:
                # If there is shorted path to v through u.
                if dist[v] > dist[u] + weight:
                    # Updating distance of v
                    dist[v] = dist[u] + weight
                    trace[v] = u
                    heapq.heappush(pq, (dist[v], v))
 
        # traceback path and return dist[t]
        ans = []
        a =t
        while a!=s:
            ans.insert(0,a)
            a = trace[a]
        ans.insert(0,s)
        return ans,dist[t]

def find_nearest_node(node,u,v):
    x = v[0]-u[0]
    y = v[1]-u[1]
    res = float('inf')
    id = -1
    for i in range(6):
        dis = distance([u[0]+x/5*i,u[1]+y/5*i], node)
        if dis < res:
            res = dis
            id = i
    return [u[0]+x/5*id,u[1]+y/5*id]

def find_way(s,t):
    # create the graph from dataset

    # take all vertex
    V = read_data("./Dataset/data_node_2.txt")
    V.insert(0, [0])
    g = Graph(len(V)+5)
    n = len(V)-1
    
    # take all edge
    E = read_data("./Dataset/data_distance_2.txt")
    nearest_node = [[-1,-1],[-1,-1]]
    nearest_node_id = [-1,-1]
    for i in range(len(E)):
        # add edge to graph
        node = E[i]
        coords_1 = V[node[0]]
        coords_2 = V[node[1]]
        g.addEdge( node[0], node[1], distance(coords_1, coords_2))

        # find nearest vertex of s and t for V
        S = find_nearest_node(s,coords_1,coords_2)
        T = find_nearest_node(t,coords_1,coords_2)
        if nearest_node[0][0] == -1 or distance(s, nearest_node[0]) > distance(s, S):
            nearest_node[0] = S
            nearest_node_id[0] = i
        if nearest_node[1][0] == -1 or distance(t, nearest_node[1]) > distance(t, T):
            nearest_node[1] = T
            nearest_node_id[1] = i
    
    # add edge to the nearest vertex of s and t
    for i in range(2):
        u = E[nearest_node_id[0]][i]
        g.addEdge( n+1, u, distance(nearest_node[0], V[u]))
        v = E[nearest_node_id[1]][i]
        g.addEdge( n+2, v, distance(nearest_node[1], V[v]))

    # add 2 nearest vertex to V
    V.append(nearest_node[0])
    V.append(nearest_node[1])

    # find shortest path from s to t
    ans,dis = g.shortestPath(n+1,n+2)
    coords = []
    for i in ans:
        node = V[i]
        coords.append(node)
    return coords,dis