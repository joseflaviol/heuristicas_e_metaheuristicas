class MaxHeap:

    def __init__(self, tamanho_maximo):
        self.tamanho_maximo = tamanho_maximo
        self.tamanho = 0
        self.heap = [None] * tamanho_maximo 

    def pai(self, i):
        return (i - 1) / 2
    
    def esquerda(self, i):
        return (2 * i) + 1
    
    def direita(self, i):
        return (2 * i) + 2
 
    def insere(self, item):
        if self.tamanho >= self.tamanho_maximo:
            return 
        
        self.tamanho += 1
        self.heap[self.tamanho - 1] = item 

        i = self.tamanho - 1

        while i != 0 and self.heap[pai(i)].razao < self.heap[i].razao: 
            aux = self.heap[pai(i)]
            self.heap[pai(i)] = self.heap[i]
            self.heap[i] = aux

            i = pai(i)    
    
    # versão modificada da árvore heap
    def extrai(self, indice):  
        item = self.heap[indice]
        self.tamanho -= 1
        self.heap[indice] = self.heap[self.tamanho]

        while True:
            maior = indice

            if self.esquerda(indice) < self.tamanho and self.heap[self.esquerda(indice)].razao > self.heap[indice].razao:
                maior = self.esquerda(indice)
            
            if self.direita(indice) < self.tamanho and self.heap[self.direita(indice)].razao > self.heap[maior].razao:
                maior = self.direita(indice)

            if maior == indice:
                break
            
            aux = self.heap[maior]
            self.heap[maior] = self.heap[indice]
            self.heap[indice] = aux 
        
            indice = maior

        return item    