class Tupla():
    def __init__(self):
        self._cols = []
        #Lista de Strings de tamanho qtd_colunas
    
    def adicionar_atributo(self, atrib):
        self._cols.append(atrib)
    
    def recuperar_tupla(self):
        return self._cols