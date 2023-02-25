import time
from graph import Graph
from npe import NPE
from kruskal import kruskal
from math import sqrt
import numpy as np

def distancia(p, q):
    return sqrt( pow( p[0] - q[0], 2 ) + pow(p[1] - q[1], 2 ) )

def fitness(x):
    f = 0
    n = x.n
    d = x.d
    degree = x.degree
    N = len(n)
    degree_list = [0] * N  
    lookup = [n[0]] * N
    m = 0

    for i in range(1, N):
        j = lookup[d[i] - 1]
        degree_list[j] += 1
        degree_list[n[i]] += 1
        if degree_list[j] > degree or degree_list[n[i]] > degree:
            m += 1
        f += x.G.adj(j)[n[i]] + m * f
        lookup[d[i]] = n[i]

    return f

def simulated_annealing(fitness, x0, temp, cooling_factor, n_iter):
    x_current = x0
    f_current = fitness(x_current)
    T = temp 

    x_best = x_current
    f_best = f_current

    t_end = time.time() + 60
    t_start = time.time()
    while time.time() < t_end:
        r = np.random.rand()

        oN, oD = x_current.get()

        if r < 0.5:
            N, D = x_current.SPRN()
        else:
            N, D = x_current.TBRN()
    
        x_new = x_current
        x_new.setN(N)
        x_new.setD(D)

        f_new = fitness(x_new)

        p_accept = np.exp(-(f_new - f_current) / T)

        if np.random.rand() < p_accept:
            x_current = x_new
            f_current = f_new
        else:
            x_current.setN(oN)
            x_current.setD(oD)

        if f_current < f_best:
            x_best = x_current
            f_best = f_current

        with open('%dsec.txt' % (int(t_end - t_start)), 'a+') as f:
            f.write('%.2f %.2f\n' % (time.time() - t_start, f_best))
        
        T *= cooling_factor
    
    return x_best, f_best

def main():

    coordenadas = []

    while True:
        try:
            #_, x, y = (int(x) for x in input().split())
            x, y = (int(x) for x in input().split())
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

    x0 = NPE(g, degree = 5)
    temp = 20 
    cooling_factor = 0.99 
    n_iter = 15000

    x_best, f_best = simulated_annealing(fitness, x0, temp, cooling_factor, n_iter)

    print("Best solution found:", x_best)
    print("Objective function value at best solution: %.2f" % (f_best))
    '''
    npe = NPE(g, degree = 5)

    _, fit = npe.decode()
    
    best_fit = fit

    t = 0
    while t < 5000:
        r = np.random.rand()
        
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
        else:
            npe.setN(oN)
            npe.setD(oD)

        t += 1
    
    print('Best fit: %.2f' % (best_fit))
    '''

main()