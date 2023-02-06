import random
from graph import Graph
from npe import NPE
from kruskal import kruskal

def main():

    vertices, edges = (int(x) for x in input().split())

    edges_list = []

    g = Graph(vertices)

    for _ in range(edges):
        discard, u, v, w = (x for x in input().split())

        g.addEdge(int(u) - 1, int(v) - 1, int(w))
        edges_list.append( (int(u) - 1, int(v) - 1, int(w)) )

    mst = kruskal(vertices, sorted(edges_list, key = lambda x: x[2]))

    print(f'mst: {mst}')

    npe = NPE(g, degree = 3)

    _, fit = npe.decode()
    
    best_fit = fit

    t = 0
    while t < 1000:
        r = random.random()
        
        oN, oD = npe.get()

        if r < 0.5:        
            N, D = npe.SPRN()
        else:
            N, D = npe.TBRN()

        npe.setN(N)
        npe.setD(D)

        _, fit = npe.decode()

        if fit < best_fit:
            best_fit = fit
            print(best_fit)
        else:
            npe.setN(oN)
            npe.setD(oD)

        t += 1

main()