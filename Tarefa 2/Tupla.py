class Tupla():
    def __init__(self):
        self._cols = []
        #Lista de Strings de tamanho qtd_colunas
    
    def adicionar_atributo(self, atrib):
        colunas = atrib.split(',')
        self._cols= colunas
    
    @property
    def cols(self):
        return self._cols
        