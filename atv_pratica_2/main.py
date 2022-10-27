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

def ordena(itens):
    for i in range(1, len(itens)):
        chave = itens[i]
        j = i - 1

        while j > -1 and chave.razao > itens[j].razao:
            itens[j + 1] = itens[j]
            j = j - 1 

        itens[j + 1] = chave 

    return itens             

def remove_itens_inviaveis(itens, capacidade_utilizada, capacidade_da_mochila):
    n_itens = []
    for item in itens:
        if (capacidade_utilizada + item.peso) <= capacidade_da_mochila:
            n_itens.append(item)
    return n_itens    

def construcao_semi_gulosa_aleatoria(itens, capacidade_da_mochila):
    solucao = []
    capacidade_utilizada = 0
    c = ordena(itens)

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