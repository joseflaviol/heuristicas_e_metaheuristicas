class UF:
    
    def __init__(self, vertices):
        self.vertices = vertices
        self.altura = [0] * vertices
        self.chefe = [int(x) for x in range(vertices)]
    
    def find(self, u):
        while u != self.chefe[u]:
            u = self.chefe[u]
        return u

    def union(self, r, s):
        if self.altura[r] > self.altura[s]:
            self.chefe[s] = r 
        else:
            self.chefe[r] = s
            if self.altura[r] == self.altura[s]:
                self.altura[s] = self.altura[r] + 1

def kruskal(vertices, arestas):
    uf = UF(vertices)

    arvore = []
    custo = 0

    for a in arestas:
        find_u = uf.find(a[0])
        find_v = uf.find(a[1])

        if find_u != find_v:
            uf.union(find_u, find_v)
            custo += a[2]
            arvore.append(a)
    
    return custo