import sys
import numpy as np 

class Item:

    def __init__(self, peso, beneficio):
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

        itens.append( Item(int(linha[1]), int(linha[0])) )

    f.close()

    return (itens, capacidade_da_mochila, numero_de_itens) 

def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
 
    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)
 
    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]
 
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
 
    i = 0    
    j = 0     
    k = l    
 
    while i < n1 and j < n2:
        if L[i].razao > R[j].razao:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
 
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def merge_sort(arr, l, r):
    if l < r:
        m = l+(r-l)//2
 
        merge_sort(arr, l, m)
        merge_sort(arr, m+1, r)
        merge(arr, l, m, r)         

def remove_itens_inviaveis(itens, capacidade_utilizada, capacidade_da_mochila):
    n_itens = []
    for item in itens:
        if (capacidade_utilizada + item.peso) <= capacidade_da_mochila:
            n_itens.append(item)
    return n_itens    

def construcao_semi_gulosa_aleatoria(itens, capacidade_da_mochila):
    solucao = []
    capacidade_utilizada = 0
    c = itens.copy()
    merge_sort(c, 0, len(c) - 1)

    while len(c) > 0:
        pct = int((len(c) * 1) / 100)
        if pct == 0:
            pct += 1
        s = np.random.randint( pct )
        capacidade_utilizada += c[s].peso
        solucao.append(c[s])
        c.pop(s)
        c = remove_itens_inviaveis(c, capacidade_utilizada, capacidade_da_mochila)

    return solucao

def main():

    itens, capacidade_da_mochila, numero_de_itens = carrega_itens(sys.argv[1])

    s = construcao_semi_gulosa_aleatoria(itens, capacidade_da_mochila)
    soma_beneficio = 0
    soma_peso = 0

    for item in s:
        soma_beneficio += item.beneficio
        soma_peso += item.peso
        #print(item)
    
    print("Solucao:")
    print("\tBeneficio: %d\n\tPeso: %d\n" % (soma_beneficio, soma_peso))

main()