import random, time
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

def adj(g, p1):
    l = []

    for _ in range(g.v):
        l.append([])

    for e in p1:
        u, v, w = e 
        l[u].append(v)
        l[v].append(u)

    return l

def seleciona(populacao, avaliacoes):
    ix = random.randint(0, len(populacao) - 1)
    iy = random.randint(0, len(populacao) - 1)

    if avaliacoes[ix] > avaliacoes[iy]:
        return ix 
    else:
        return iy

def combina(g, p1, p2, d):
    lp1 = adj(g, p1)
    lp2 = adj(g, p2)

    T = []
    S = []
    degree = [0] * g.v 
    marcado = [False] * g.v
    
    v1 = random.randint(0, g.v - 1)
    marcado[v1] = True

    S.append(v1)

    prob = (1 / fitness(p1)) / ( 1 / fitness(p1) + 1 / fitness(p2) )    

    u = random.random()

    v2 = None
    if u < prob:
        v2 = random.choice(lp1[v1])
    else:
        v2 = random.choice(lp2[v1])

    marcado[v2] = True
    S.append(v2)
    T.append( (v1, v2, g.custo(v1, v2)) )
    degree[v1] = 1
    degree[v2] = 1
    while len(S) != g.v:
        u = random.random()

        if u < prob:
            ok = False
            for i in S:
                if degree[i] < d:
                    j = random.choice(lp1[i])
                    if not marcado[j]:
                        marcado[j] = True 
                        S.append(j)
                        T.append( (i, j, g.custo(i, j)) )
                        degree[i] += 1
                        degree[j] += 1
                        ok = True
                        break
            if not ok:
                for i in S:
                    if degree[i] < d:
                        j = random.choice(lp2[i])
                        if not marcado[j]:
                            marcado[j] = True 
                            S.append(j)
                            T.append( (i, j, g.custo(i, j)) )
                            degree[i] += 1
                            degree[j] += 1
                            ok = True
                            break       
                aux = 0                 
                while not ok or aux < 10:
                    i = random.choice(S)
                    if degree[i] < d:
                        j = random.choice(list(g.adj(i).keys()))
                        if not marcado[j]:
                            marcado[j] = True
                            S.append(j)
                            T.append( (i, j, g.custo(i, j)) )
                            degree[i] += 1
                            degree[j] += 1
                            ok = True 
                        aux += 1
        else:
            ok = False
            for i in S:
                if degree[i] < d:
                    j = random.choice(lp2[i])
                    if not marcado[j]:
                        marcado[j] = True 
                        S.append(j)
                        T.append( (i, j, g.custo(i, j)) )
                        degree[i] += 1
                        degree[j] += 1
                        ok = True
                        break
            if not ok:
                for i in S:
                    if degree[i] < d:
                        j = random.choice(lp1[i])
                        if not marcado[j]:
                            marcado[j] = True 
                            S.append(j)
                            T.append( (i, j, g.custo(i, j)) )
                            degree[i] += 1
                            degree[j] += 1
                            ok = True
                            break       
                aux = 0     
                while not ok or aux < 10:
                    i = random.choice(S)
                    if degree[i] < d:
                        j = random.choice(list(g.adj(i).keys()))
                        if not marcado[j]:
                            marcado[j] = True
                            S.append(j)
                            T.append( (i, j, g.custo(i, j)) )
                            degree[i] += 1
                            degree[j] += 1
                            ok = True                 
                    aux += 1
    return T

def evolui(g, d, populacao):
    nova_populacao = []

    for i in range(99):
        ix = seleciona(populacao)
        iy = seleciona(populacao)
        nova_populacao.append(combina(g, populacao[ix], populacao[iy], d))

    return nova_populacao

def melhor(populacao):
    avaliacoes = []
    m = 10000000000000
    mi = 0
    for i in range(len(populacao)):
        fi = fitness(populacao[i])
        if fi < m:
            m = fi
            mi = i
        avaliacoes.append(fi)
    return (avaliacoes, mi)

def evolutivo(g, d):
    populacao = []

    for _ in range(100):
        populacao.append( prim(g, d) )

    avaliacoes, idx_melhor = melhor(populacao)

    t_end = time.time() + 60
    while time.time() < t_end:
        u = random.random()

        if u < 0.7:
            ix = seleciona(populacao, avaliacoes)    
            iy = seleciona(populacao, avaliacoes)
            filho = combina(g, populacao[ix], populacao[iy], d)
            fit_filho = fitness(filho)
            iz = random.randint(0, len(populacao) - 1)

            if iz != idx_melhor and fit_filho < avaliacoes[iz]:
                populacao[iz] = filho
                avaliacoes[iz] = fit_filho
                if fit_filho < avaliacoes[idx_melhor]:
                    idx_melhor = iz 
    
        print("Melhor: %.2f" % (avaliacoes[idx_melhor]))

def main():
    coordenadas = []

    while True:
        try:
            x, y = (int(x) for x in input().split())
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
    
    evolutivo(g, 5)
    #print('Mst: %.2f' % (mst))

    

    #for i in range(30):
    #    print('Custo: %.2f' % (fitness(populacao[i])))

main()