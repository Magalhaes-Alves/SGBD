from Tupla import Tupla
"""
    Esquema das páginas
    
    qntd_de_tuplas: int
    Um registro em cada linha    
"""

class Pagina():
    def __init__(self):
        self._tuplas = []
        #Lista de tuplas com 12, no máximo
        self._qtd_tuplas_ocup = 0
        #self._nome_página = nome_arquivo

    def adicionar_tupla(self,tupla):
        if (self._qtd_tuplas_ocup <12): 
            self._tuplas.append(tupla.cols)           
            self._qtd_tuplas_ocup+=1

            return True
        else:
            return False

"""     def gravar(self):
        with open(self._nome_página+".txt","w") as saida:
            saida.write(str(self._qtd_tuplas_ocup) + "\n")
            for i in self._tuplas:
                saida.write(i+"\n") """
