import sys, random
from MaxHeap import MaxHeap

'''
    TO DO
        1 - ler instancia -> feito
        2 - heuristica construtiva aleatorizada
        3 - max heap na construtiva
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

def construtiva(itens_ordenados, capacidade):
    solucao = [0] * len(itens_ordenados)
    beneficio_solucao = 0
    capacidade_utilizada = 0

    mh = MaxHeap(itens_ordenados.copy())

    while not mh.vazia():
        pct = 0.2 * mh.tamanho

        if pct == 0:
            pct = 1

        idx = random.randint(0, int(pct))

        item = mh.extrai(idx)

        if item.peso + capacidade_utilizada <= capacidade:

            solucao[item.indice] = 1
            beneficio_solucao += item.beneficio
            capacidade_utilizada += item.peso
        
    return solucao

'''
    retorna beneficios
'''
def avalia(populacao, itens, p, capacidade):
    
    melhor = 0
    avaliacoes = []
    
    for individuo in populacao:
        peso = 0
        penalidade = 0
        
        for i in range(len(individuo)):
            peso += individuo[i] * itens[i].peso 
            penalidade += individuo[i] * itens[i].peso - capacidade
        
        if peso <= capacidade:
            penalidade = 0
        else:
            penalidade *= p

        beneficio = 0
        
        for i in range(len(individuo)):
            beneficio += individuo[i] * itens[i].beneficio - penalidade
        
        if beneficio > melhor:
            melhor = beneficio
        
        avaliacoes.append(beneficio)
    
    return avaliacoes, melhor

def torneio(populacao, avaliacoes):
    melhor = 0
    
    for _ in range(5):
        x = random.randint(0, len(populacao) - 1)
        if avaliacoes[x] > avaliacoes[melhor]:
            melhor = x 

    return populacao[melhor]

def progenitores(populacao, avaliacoes):
    p = []

    for _ in range(len(populacao)):
        p.append(torneio(populacao, avaliacoes))

    return p

def recombina(p, taxa):
    
    i = 0
    prox_geracao = []
    while i < len(p):
        x = i 
        y = i + 1

        if random.randint(0, 9) <= taxa:
            ponto = random.randint(0, len(p[x]) - 1)
            xy = []
            yx = []
            for j in range(ponto):
                xy.append(p[x][j])
                yx.append(p[y][j])
            for j in range(ponto, len(p[x])):
                xy.append(p[y][j])
                yx.append(p[x][j])
            prox_geracao.append(xy)
            prox_geracao.append(yx)
        else:
            prox_geracao.append(p[x])
            prox_geracao.append(p[y])

        i += 2 
    return prox_geracao

def genetico(itens, itens_ordenados, capacidade):
    tam_populacao = 50
    populacao = []

    for _ in range(tam_populacao):
        populacao.append(construtiva(itens_ordenados, capacidade))
    
    m = 0
    t = 0
    while t < 50:
        avaliacoes, melhor = avalia(populacao, itens, itens_ordenados[0].razao, capacidade)
        print(melhor)
        if melhor > m:
            m = melhor
        p = progenitores(populacao, avaliacoes)

        prox_geracao = recombina(p, 7) 
        #muta(prox_geracao)

        populacao = prox_geracao
        t += 1

    return m

def main():
    nome_arq = sys.argv[1]

    itens, n_itens, capacidade = carrega_itens(nome_arq)
    itens_ordenados = sorted(itens, key = lambda x: x.razao, reverse = True)

    m = genetico(itens, itens_ordenados, capacidade)

main()