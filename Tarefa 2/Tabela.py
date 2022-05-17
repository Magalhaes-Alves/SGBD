import Esquema

class Tabela():

    def __init__(self, nome_arq):
        self._pages = []
        #Lista de Paginas
        self._qtd_paginas = 0
        self._esquema = 0
        self._nome_arq = nome_arq

    @property
    def esquema(self):
        return self._esquema
    
    @esquema.setter
    def esquema(self,esquema):
        self._esquema = esquema
    
    def carregarDados(self):
        with open(self._nome_arq,"r") as arq:
            linhas = arq.readlines
        
        nome_colunas = linhas[0][:-1].split(',')
        registros = linhas[1:]

        esq = Esquema(nome_colunas)
        self.esquema = esq
