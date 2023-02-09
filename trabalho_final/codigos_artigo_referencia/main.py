from grafo import Grafo
from prim import prim
from kruskal import kruskal
from math import sqrt

def distancia(p, q):
    return sqrt( pow( p[0] - q[0], 2 ) + pow(p[1] - q[1], 2 ) )

def fitness(solucao):
    custo = 0

    for aresta in solucao:
        custo += aresta[2]

    return custo

def combina(p1, p2):
    

def main():
    coordenadas = []

    while True:
        try:
            _, x, y = (int(x) for x in input().split())
            coordenadas.append( (x, y) )
        except EOFError:
            break

    g = Grafo(len(coordenadas))
    arestas = []

    for i in range(len(coordenadas)):
        for j in range(i + 1, len(coordenadas)):
            g.add(i, j, distancia( coordenadas[i], coordenadas[j] ))
            arestas.append( (i, j, g.custo(i, j)) )

    mst = kruskal(g.v, sorted(arestas, key = lambda x: x[2]))
    print('Mst: %.2f' % (mst))

    populacao = []

    for _ in range(30):
        populacao.append( prim(g, 5) )

    for i in range(30):
        print('Custo: %.2f' % (fitness(populacao[i])))

main()