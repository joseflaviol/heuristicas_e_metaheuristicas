import random
from graph import Graph
from npe import NPE
from kruskal import kruskal
from math import sqrt

def distancia(p, q):
    return sqrt( pow( p[0] - q[0], 2 ) + pow(p[1] - q[1], 2 ) )

def main():

    '''vertices, edges = (int(x) for x in input().split())

    edges_list = []

    g = Graph(vertices)

    for _ in range(edges):
        discard, u, v, w = (x for x in input().split())

        g.addEdge(int(u) - 1, int(v) - 1, int(w))
        edges_list.append( (int(u) - 1, int(v) - 1, int(w)) )
    '''
    coordenadas = []

    while True:
        try:
            _, x, y = (int(x) for x in input().split())
            coordenadas.append( (x, y) )
        except EOFError:
            break

    g = Graph(len(coordenadas))
    edges_list = []

    for i in range(len(coordenadas)):
        for j in range(i + 1, len(coordenadas)):
            g.addEdge(i, j, distancia( coordenadas[i], coordenadas[j] ))
            edges_list.append( (i, j, g.weight(i, j)) )

    mst = kruskal(g.v, sorted(edges_list, key = lambda x: x[2]))

    print('Mst: %.2f' % (mst))

    npe = NPE(g, degree = 5)

    _, fit = npe.decode()
    
    best_fit = fit

    t = 0
    while t < 50000:
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
            #print(best_fit)
        else:
            npe.setN(oN)
            npe.setD(oD)

        t += 1
    
    print('Best fit: %.2f' % (best_fit))

main()