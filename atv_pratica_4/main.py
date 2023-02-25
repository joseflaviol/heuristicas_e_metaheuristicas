import sys, random
from MaxHeap import MaxHeap

'''
    TO DO
        1 - ler instancia -> feito
        2 - heuristica construtiva aleatorizada -> feito
        3 - max heap na construtiva -> feito
'''

class Item:

    def __init__(self, indice, beneficio, peso):
        self.indice = indice
        self.beneficio = beneficio 
        self.peso = peso 
        self.razao = beneficio / peso

def carrega_itens(nome_arq):
    arq = open(nome_arq, 'r')

    n_itens, capacidade = (int(x) for x in arq.readline().split())
    itens = []

    for i in range(n_itens):
        beneficio, peso = (int(x) for x in arq.readline().split())

        itens.append( Item(i, beneficio, peso) )
    
    arq.close()

    return (itens, n_itens, capacidade)

def aleatoria(t_itens):
    solucao = [0] * t_itens
    for i in range(t_itens):
        if random.randint(0, 9) % 2:
            solucao[i] = 1
    return solucao

def construtiva(itens_ordenados, capacidade):
    solucao = [0] * len(itens_ordenados)
    beneficio_solucao = 0
    capacidade_utilizada = 0

    mh = MaxHeap(itens_ordenados.copy())

    while not mh.vazia():
        pct = 0.1 * mh.tamanho

        if pct == 0:
            pct = 1

        idx = random.randint(0, int(pct))

        item = mh.extrai(idx)

        if item.peso + capacidade_utilizada <= capacidade:

            solucao[item.indice] = 1
            beneficio_solucao += item.beneficio
            capacidade_utilizada += item.peso
        
    return solucao

def avalia(populacao, itens, p, capacidade):

    idx_melhor = 0    
    melhor = 0
    avaliacoes = []
    
    for individuo in populacao:
        peso = 0
        penalidade = 0
        
        for i in range(len(individuo)):
            penalidade += individuo[i] * itens[i].peso
        
        if penalidade <= capacidade:
            penalidade = 0
        else:
            penalidade -= capacidade
            penalidade *= p

        beneficio = 0
        
        for i in range(len(individuo)):
            beneficio += individuo[i] * itens[i].beneficio - penalidade
        
        if beneficio > melhor:
            idx_melhor = len(avaliacoes)
            melhor = beneficio
        
        avaliacoes.append(beneficio)

    return avaliacoes, idx_melhor
    
def seleciona(populacao, avaliacoes):
    x = random.randint(0, len(populacao) - 1)
    y = random.randint(0, len(populacao) - 1)

    if avaliacoes[x] > avaliacoes[y]:
        return x 

    return y

def recombina(p1, p2):
    c = []

    ponto = random.randint(0, len(p1) - 1)

    for i in range(0, ponto):
        c.append(p1[i])

    for i in range(ponto, len(p2)):
        c.append(p2[i])

    return c

def muta(individuo):
    bit = random.randint(0, len(individuo) - 1)

    if individuo[bit] == 1:
        individuo[bit] = 0
    else:
        individuo[bit] = 1

def evolui(populacao, avaliacoes, melhor):
    prox_geracao = [populacao[melhor].copy()]

    for _ in range(len(populacao)):
        p1 = seleciona(populacao, avaliacoes)
        p2 = seleciona(populacao, avaliacoes)

        tx = random.random()
        c = None

        if tx <= 0.8:
            c = recombina(populacao[p1], populacao[p2])
        else:
            if avaliacoes[p1] > avaliacoes[p2]:
                c = populacao[p1].copy()
            else:
                c = populacao[p2].copy()

        tx = random.random()

        if tx <= 0.002:
            muta(c)

        prox_geracao.append(c)
    
    return prox_geracao

def genetico(itens, itens_ordenados, capacidade):
    tam_populacao = 50
    populacao = []

    for _ in range(tam_populacao):
        populacao.append(construtiva(itens_ordenados, capacidade))
    
    m = 0
    t = 0
    
    while t < 20:
        avaliacoes, idx_melhor = avalia(populacao, itens, itens_ordenados[0].razao, capacidade)
        print("%dº geracao: %d" %(t, avaliacoes[idx_melhor]))
        if avaliacoes[idx_melhor] > m:
            m = avaliacoes[idx_melhor]
        prox_geracao = evolui(populacao, avaliacoes, idx_melhor)        
        t += 1

    return m

def main():
    nome_arq = sys.argv[1]

    itens, n_itens, capacidade = carrega_itens(nome_arq)
    itens_ordenados = sorted(itens, key = lambda x: x.razao, reverse = True)

    m = genetico(itens, itens_ordenados, capacidade)

main()