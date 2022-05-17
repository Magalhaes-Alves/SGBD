from re import I


class Esquema():
    def __init__(self, nome_colunas):
        self._qtd_cols = len(nome_colunas)
        self._nome_para_indice = {}
        aux = 0
        for nome_coluna in nome_colunas:
            self._nome_para_indice[nome_coluna] = aux
            aux += 1

    @property
    def qtd_cols(self):
        return self._qtd_cols

    @property
    def nome_para_indice(self):
        return self._nome_para_indice