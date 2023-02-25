'''
    Utilizado para gerar a população inicial
    Solução representada como conjunto de arestas
'''

import random

#g = grafo completo
#d = grau máximo
def prim(g, d):
    T = []
    S = []
    U = list(range(g.v))

    marcados = [0] * g.v
    grau = [0] * g.v

    idx = random.randint(0, len(U) - 1)
    v1 = U[idx]

    marcados[v1] = 1
    S.append(v1)
    U.pop(idx)

    while U:
        ix = random.randint(0, len(U) - 1)  
        x = U[ix]

        iy = None
        y = None

        while iy == None:
          iy = random.randint(0, len(S) - 1)
          y = S[iy]

          if grau[y] == d:
              iy = None
        
        T.append( ( x, y, g.custo(x, y) ))
        grau[x] += 1
        grau[y] += 1
        marcados[x] = 1

        S.append(x)
        U.pop(ix)
    
    return T