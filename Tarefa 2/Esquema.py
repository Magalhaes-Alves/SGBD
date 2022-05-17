class Esquema():
    def __init__(self, nome_colunas):
        self._qtd_cols = len(nome_colunas)
        self._nome_para_indice = ""

    @property
    def qtd_cols(self):
        return self._qtd_cols