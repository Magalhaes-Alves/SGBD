from dbm import dumb
from sys import prefix
from Esquema import Esquema
from Tupla import Tupla
from Pagina import Pagina
import pickle

class Tabela():

    def __init__(self, nome_arq):
        self._pages = []
        #Lista de Paginas
        self._qtd_paginas = 0
        self._esquema = 0
        self._nome_arq = nome_arq

    @property
    def pages(self):
        return self._pages
    
    @pages.setter
    def pages(self,pages):
        self._pages = pages

    @property
    def qtd_paginas(self):
        return self._qtd_paginas
    
    @qtd_paginas.setter
    def qtd_paginas(self,qtd_paginas):
        self._qtd_paginas = qtd_paginas

    @property
    def nome_arq(self):
        return self._nome_arq
    
    @nome_arq.setter
    def nome_arq(self,nome_arq):
        self._nome_arq = nome_arq
    
    @property
    def esquema(self):
        return self._esquema
    
    @esquema.setter
    def esquema(self,esquema):
        self._esquema = esquema
    
    def adicionaPagina(self, pagina):
        self._pages.append(pagina)

        self._qtd_paginas += 1
    

    def carregarDados(self):
        prefixo = self._nome_arq.split(".")[0]
        #print(prefixo)
        with open(self._nome_arq,"r") as arq:
            linhas = arq.readlines()
        
        nome_colunas = linhas[0][:-1].split(',')
        registros = linhas[1:]

        esq = Esquema(nome_colunas)
        self.esquema = esq
        

        page = Pagina()
        for registro in registros:
            tupla = Tupla()

            tupla.adicionar_atributo(registro[:-1])

            if(not page.adicionar_tupla(tupla)):
                nome_arquivo =prefixo+"_"+"pagina"+"_"+str(self._qtd_paginas)+".txt"
                self.adicionaPagina(nome_arquivo)
            
                self.serializador(page,nome_arquivo)
            
                page = Pagina()

                page.adicionar_tupla(tupla)

        if(len(page.tuplas)>0):
            nome_arquivo =prefixo+"_"+"pagina"+"_"+str(self._qtd_paginas)+".txt"
            self.adicionaPagina(nome_arquivo)
            self.serializador(page,nome_arquivo)
        
        self.serializador(self, prefixo+"_tabela")

    
    def PrintarPaginas(self):
        for page in self._pages[0]._tuplas:
            print(page)
            
    def serializador(self,objeto, nome):
        with open(nome,"wb") as arq:
            pickle.dump(objeto,arq)

    def deserializador(self, nome):
        with open(nome,"rb") as arq:
           return pickle.load(arq) 
