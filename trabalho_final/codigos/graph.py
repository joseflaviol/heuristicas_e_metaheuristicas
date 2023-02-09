class Graph:

    def __init__(self, v):
        self.v = v
        self.adj_list = []
        for _ in range(v):
            self.adj_list.append({})       

    def addEdge(self, u, v, w = 1):
        self.adj_list[u][v] = w 
        self.adj_list[v][u] = w

    def adj(self, u):
        return self.adj_list[u]
    
    def weight(self, u, v):
        return self.adj_list[u][v]