class Grafo:

    def __init__(self, v):
        self.v = v
        self.lista_adj = []
        for _ in range(v):
            self.lista_adj.append({})
    
    def add(self, u, v, w):
        self.lista_adj[u][v] = w 
        self.lista_adj[v][u] = w
    
    def adj(self, u):
        return self.lista_adj[u]
    
    def custo(self, u, v):
        return self.lista_adj[u][v]