import sys
import numpy as np 
from maxHeap import MaxHeap

class Item:

    def __init__(self, indice, peso, beneficio):
        self.indice = indice
        self.peso = peso
        self.beneficio = beneficio
        self.razao = beneficio / peso
    
    def __str__(self):
        s = ("Peso: %d\nBeneficio: %d\nRazao: %.2f\n" % (self.peso, self.beneficio, self.razao) )
        return s

def carrega_itens(nome_arq):

    numero_de_itens = None
    capacidade_da_mochila = None 
    itens = []

    f = open(nome_arq, "r")

    linha = f.readline().split()

    numero_de_itens = int(linha[0])
    capacidade_da_mochila = int(linha[1])

    for i in range(numero_de_itens):

        linha = f.readline().split()

        itens.append( Item(i, int(linha[1]), int(linha[0])) )

    f.close()

    return (itens, capacidade_da_mochila, numero_de_itens) 

def aleatoriedade(n):
    if n < 1000:
        return 5
    if n < 5000:
        return 2
    return 1

def construtiva(itens_ordenados, capacidade_da_mochila, numero_de_itens):
    
    capacidade_utilizada = 0
    beneficio_total = 0
    solucao = [0] * numero_de_itens
    max_heap = MaxHeap(len(itens_ordenados))
    max_heap.tamanho = len(itens_ordenados)
    max_heap.heap = itens_ordenados.copy()
    a = aleatoriedade(numero_de_itens) / 100

    while max_heap.tamanho > 0:
        pct = int(max_heap.tamanho * a)
        
        if pct == 0:
            pct += 1
        
        s = np.random.randint( pct )  

        item = max_heap.extrai(s)

        if capacidade_utilizada + item.peso <= capacidade_da_mochila:
            solucao[item.indice] = 1
            capacidade_utilizada += item.peso
            beneficio_total += item.beneficio

    return (solucao, beneficio_total, capacidade_utilizada)

def busca_local(itens, s, beneficio, peso):
    
    for i in range((43 * len(itens)) // 100):
        j = np.random.randint(len(itens)) 
        if s[j] == 1:
            beneficio -= itens[j].beneficio
            peso -= itens[j].peso 
            s[j] = 0 
        else:
            beneficio += itens[j].beneficio
            peso += itens[j].peso 
            s[j] = 1

    return (s, beneficio, peso)     

def grasp(itens, itens_ordenados, capacidade_da_mochila):
    x, beneficio_x, peso_x = construtiva(itens_ordenados, capacidade_da_mochila, len(itens))

    i = 0
    while i < 100:
        y, beneficio_y, peso_y = construtiva(itens_ordenados, capacidade_da_mochila, len(itens))

        y = busca_local(itens, y, beneficio_y, peso_y)

        if beneficio_x < beneficio_y and peso_y <= capacidade_da_mochila:
            print("%d -> %d" % (beneficio_x, beneficio_y))
            beneficio_x = beneficio_y
            peso_x = peso_y
            x = y

        i += 1

    return (x, beneficio_x, peso_x)    

def limite_superior(n):
    if n < 1000:
        return n
    elif n < 5000:
        return n // 4
    
    return n // 7

def main():

    itens, capacidade_da_mochila, numero_de_itens = carrega_itens(sys.argv[1])

    c = sorted(itens, key = lambda x: x.razao, reverse = True)[0: limite_superior(len(itens)) ]

    s, soma_beneficio, soma_peso = grasp(itens, c, capacidade_da_mochila)

    print("Solucao:")
    print("\tBeneficio: %d\n\tPeso: %d\n" % (soma_beneficio, soma_peso))

main()