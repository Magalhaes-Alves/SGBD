class Esquema():
    def __init__(self, nome_colunas):
        self._qtd_cols = len(nome_colunas)
        self._nome_para_indice = {}
        aux = 0
        for nome_coluna in nome_colunas:
            self._nome_para_indice[nome_coluna] = aux
            #Adiciona a tupla [nome_coluna : aux ] ao dicionário, sendo nome_coluna colocada como chave e o 
            #aux o indice associado a essa chave
            aux += 1

    @property
    def qtd_cols(self):
        return self._qtd_cols

    @property
    def nome_para_indice(self):
        return self._nome_para_indice