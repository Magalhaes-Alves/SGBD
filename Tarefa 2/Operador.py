from Pagina import Pagina
from Tupla import Tupla
from Tabela import Tabela
from hash import hash
from funcoes import mascara
import pickle

class Operador():

    def __init__(self,tabela1, tabela2, colTab1, colTab2):
        self._tabela1 = tabela1
        self._tabela2 = tabela2
        self.colTab1 = colTab1
        self.colTab2 = colTab2
        self.nome1 = tabela1._nome_arq.split('.')[0]
        self.nome2 = tabela2._nome_arq.split('.')[0]

    def carregarDiretorio(self, diretorioEntrada,prefixo):
        diretorio = open(prefixo + "diretorio.txt","r")

        profundidadeGlobal =int(diretorio.readline()[:-1])
        
        diretorioEntrada = []
        eof = False
        
        #Carregando os enderecos para os buckets.Nesta aplicacao, serao os nomes dos arquivos
        while(not (eof)):
            linha = diretorio.readline()
            if linha=='':
                eof=True
            else:
                diretorioEntrada.append(linha[:-1])
        return (diretorioEntrada,profundidadeGlobal)


    def aplicarhashTab2(self, tupla, chave ,diretorio2, pg2, coluna2):
        arq2 = open(self.nome2+ '_' + diretorio2[mascara(chave, pg2)] + '.txt')
        saida = open('saida.txt', 'a')
        if( chave== 27):
            print("AQUI PORRA")
        pagina2 = Pagina()
        pl_reg2 = arq2.readline().split(',')

        qtdRegistros2 = int(pl_reg2[1][:-1])

        for j in range(qtdRegistros2):
            registro2 = arq2.readline().split(',')
            registro2[len(registro2)-1] = registro2[len(registro2)-1][:-1]
            registro2 = ','.join(registro2)

            tupla2_parametro = Tupla()
            tupla2_parametro.adicionar_atributo(registro2) 
            if(not pagina2.adicionar_tupla(tupla2_parametro)):
                for tupla2 in pagina2.tuplas:
                    if(chave == int(tupla2[coluna2])):
                        if( chave== 27):
                            print("AQUI PORRA caralho")
                        saida.write(f'{",".join(tupla)},{",".join(tupla2)}\n')

                pagina2 = Pagina()
                pagina2.adicionar_tupla(tupla2_parametro)
            
        for tupla2 in pagina2.tuplas:
            if(tupla2[coluna2]==39):
                print(tupla2)
            if(chave == int(tupla2[coluna2])):
                saida.write(f'{",".join(tupla)},{",".join(tupla2)}\n')


    def juncao(self, diretorio1, diretorio2, coluna1, coluna2, pg1, pg2):
        pagina1 = Pagina()

        with open('saida.txt', 'w') as saida:
            saida.write(f'{",".join(self._tabela1.esquema.nome_para_indice.keys())},{",".join(self._tabela2.esquema.nome_para_indice.keys())}\n')

        for nomeTab1 in diretorio1:
            
            arq1 = open(self.nome1+ '_' +nomeTab1 + '.txt', 'r')
            
            pl_reg1 = arq1.readline().split(',')
            qtdRegistros1 = int(pl_reg1[1][:-1])

            for i in range(qtdRegistros1):
                registro1 = arq1.readline().split(',')
                registro1[len(registro1)-1] = registro1[len(registro1)-1][:-1]
                registro1 = ','.join(registro1)
                #print(registro1)                
                tupla1 = Tupla()
                tupla1.adicionar_atributo(registro1)

                if(not pagina1.adicionar_tupla(tupla1)):
                    for tupla in pagina1.tuplas:
                        chave = int(tupla[coluna1])
                        self.aplicarhashTab2(tupla, chave ,diretorio2, pg2, coluna2)
                        
                        pagina1 = Pagina()
                        pagina1.adicionar_tupla(tupla1)
            for tupla in pagina1.tuplas:
                chave = int(tupla[coluna1])
                if( chave== 27):
                    print("AQUI PORRA")
                self.aplicarhashTab2(tupla, chave ,diretorio2, pg2, coluna2)
        
        ids_faltantes = []
        for z in range(75):
            ids_faltantes.append(z)
        with open('saida.txt','r') as teste:
            coisas = teste.readlines()[1:]
            for coisa in coisas:
                removido = int(coisa.split(',')[0])
                ids_faltantes.remove(removido)    
        print(ids_faltantes)


    def executar(self):
        coluna1 = self._tabela1.esquema.nome_para_indice[self.colTab1]
        hash(self._tabela1, coluna1 , self.nome1 + '_')

        coluna2 = self._tabela2.esquema.nome_para_indice[self.colTab2]
        hash(self._tabela2, coluna2 , self.nome2 + '_')

        diretorio1 = []
        diretorio1,pg1 = self.carregarDiretorio(diretorio1,self.nome1 + '_')
        
        diretorio2 = []
        diretorio2,pg2 = self.carregarDiretorio(diretorio2,self.nome2 + '_')
        total = 0
        ids_faltantes = []
        for j in range(500):
            ids_faltantes.append(j)
        
        for nomeTab1 in diretorio1:
            
            arq1 = open(self.nome1+ '_' +nomeTab1 + '.txt', 'r')
            
            pl_reg1 = arq1.readline().split(',')
            quantidadeRegistros = int(pl_reg1[1][:-1])
            total += quantidadeRegistros

            for i in range(quantidadeRegistros):
                informacoes = arq1.readline().split(',')
                chavequero = int(informacoes[coluna1])
                if chavequero in ids_faltantes:
                    ids_faltantes.remove(chavequero)
        print(f"Total de registros 1 :{total}")
        print(ids_faltantes)
        self.juncao(diretorio1, diretorio2, coluna1, coluna2, pg1, pg2)