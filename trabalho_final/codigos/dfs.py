class DepthFirstSearch:

    def __init__(self, G, s, d):
        self.G = G
        self.visited = [False] * G.v 
        self.depth = [None] * G.v 
        self.depth[s] = 0
        self.degree = [0] * G.v
        self.N = []
        self.D = []
        self.dfs(s, d)

    def dfs(self, s, d): 
        
        self.visited[s] = True
        pilha = [s]

        while pilha:
            u = pilha.pop()

            self.N.append(u)
            self.D.append(self.depth[u])

            for v in self.G.adj(u):
                if not self.visited[v] and self.degree[u] < d:
                    self.visited[v] = True
                    self.depth[v] = self.depth[u] + 1 
                    pilha.append(v)
                    self.degree[u] += 1
                    self.degree[v] += 1

    def NPE(self):
        return (self.N, self.D)