from Tabela import Tabela
from hash import hash

class Operador():

    def __init__(self,tabela1, tabela2, colTab1, colTab2):
        self._tabela1 = tabela1
        self._tabela2 = tabela2
        self.colTab1 = colTab1
        self.colTab2 = colTab2
        self.nome1 = colTab1.split('_')[0]
        self.nome2 = colTab2.split('_')[0]

    def executar(self):
        coluna = self._tabela1.esquema.nome_para_indice[self.colTab1]
        print(coluna)
        #hash(self._tabela1, coluna ,self.nome1 + '_')
