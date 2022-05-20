from Pagina import Pagina
from Tupla import Tupla
from Tabela import Tabela
from hash import hash
from funcoes import mascara
import pickle
import csv
from os import remove

class Operador():

    def __init__(self,tabela1, tabela2, colTab1, colTab2):
        self._tabela1 = tabela1
        self._tabela2 = tabela2
        self.colTab1 = colTab1
        self.colTab2 = colTab2
        self.nome1 = tabela1._nome_arq.split('.')[0]
        self.nome2 = tabela2._nome_arq.split('.')[0]
        self._pages1 = []
        self._pages2 = []
        self._IO = 0
        self._numTuplas = 0

    def adicionarNumTuplas(self):
        self._numTuplas += 1


    def adicionarIO(self):
        self._IO +=1


    def adicionarNIOs(self,numIos):
        self._IO += numIos


    def numTuplasGeradas(self):
        return self._numTuplas

    
    def numIOExecutados(self):
        return self._IO


    def numPagsGeradas(self):
        return 2*len(self._pages1)


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
        
        #A partição da tabela 2 que será acessada será aberta aqui.Com a partição da tabela 1 aberta na função em que 
        #aplicarhashTab2 foi chamada , temos 2 páginas abertas(partição da tabela 1 e partição da tabela 2).
        pagina2 = Pagina()
        pl_reg2 = arq2.readline().split(',')

        qtdRegistros2 = int(pl_reg2[1][:-1])

        #Laço para ler todas as tuplas da partição correspondente
        for j in range(qtdRegistros2):
            registro2 = arq2.readline().split(',')
            registro2[len(registro2)-1] = registro2[len(registro2)-1][:-1]
            registro2 = ','.join(registro2)

            tupla2_parametro = Tupla()
            tupla2_parametro.adicionar_atributo(registro2)
            #Aqui também é usada a partição dos buckets para que só se tenha  
            if(not pagina2.adicionar_tupla(tupla2_parametro)):
                #Com a partição cheia, é feita a leitura das tuplas
                for tupla2 in pagina2.tuplas:
                    if(chave == int(tupla2[coluna2])):

                        self.adicionarNumTuplas()
                        arq_saida_pagina = self._tabela1.deserializador(self.nome1 + '_saida_' + str(len(self._pages1)-1) +'.txt')

                        tupla1parametro = Tupla()
                        tupla1parametro.adicionar_atributo(",".join(tupla))

                        tupla2parametroSaida = Tupla()
                        tupla2parametroSaida.adicionar_atributo(",".join(tupla2))

                        if(not arq_saida_pagina.adicionar_tupla(tupla1parametro)):
                            self._tabela1.serializador(arq_saida_pagina, self.nome1 + '_saida_' + str(len(self._pages1)-1) +'.txt' )
                            self.adicionarIO()
                            self._pages1.append(self.nome1 + '_saida_' + str(len(self._pages1)) +'.txt')

                            arq_saida_pagina = Pagina()
                            arq_saida_pagina.adicionar_tupla(tupla1parametro)

                            self._tabela1.serializador(arq_saida_pagina, self.nome1 + '_saida_' + str(len(self._pages1)-1) +'.txt' )
                            self.adicionarIO()
                        else:
                            self._tabela1.serializador(arq_saida_pagina, self.nome1 + '_saida_' + str(len(self._pages1)-1) +'.txt' )
                            self.adicionarIO()

                        #Abre a página de saída 2.Isto faz que a página de saída 1 seja "fechada"
                        arq_saida_pagina = self._tabela2.deserializador(self.nome2 + '_saida_' + str(len(self._pages2)-1) +'.txt')
                        if(not arq_saida_pagina.adicionar_tupla(tupla2parametroSaida)):
                            self._tabela2.serializador(arq_saida_pagina, self.nome2 + '_saida_' + str(len(self._pages2)-1) +'.txt' )
                            self.adicionarIO()

                            self._pages2.append(self.nome2 + '_saida_' + str(len(self._pages2)) +'.txt')

                            arq_saida_pagina = Pagina()
                            arq_saida_pagina.adicionar_tupla(tupla2parametroSaida)

                            self._tabela2.serializador(arq_saida_pagina, self.nome2 + '_saida_' + str(len(self._pages2)-1) +'.txt' )
                            self.adicionarIO()
                        else:
                            self._tabela2.serializador(arq_saida_pagina, self.nome2 + '_saida_' + str(len(self._pages2)-1) +'.txt' )
                            self.adicionarIO()

                pagina2 = Pagina()
                pagina2.adicionar_tupla(tupla2_parametro)
            
        for tupla2 in pagina2.tuplas:
            if(chave == int(tupla2[coluna2])):
                #Adiciona um ao número de tuplas geradas
                self.adicionarNumTuplas()
                #Carrega a página de saída 1
                arq_saida_pagina = self._tabela1.deserializador(self.nome1 + '_saida_' + str(len(self._pages1)-1) +'.txt')

                tupla1parametro = Tupla()
                tupla1parametro.adicionar_atributo(",".join(tupla))

                tupla2parametroSaida = Tupla()
                tupla2parametroSaida.adicionar_atributo(",".join(tupla2))

                if(not arq_saida_pagina.adicionar_tupla(tupla1parametro)):
                    #Escreve a página de Saída e Escreve uma nova para ser usada
                    self._tabela1.serializador(arq_saida_pagina, self.nome1 + '_saida_' + str(len(self._pages1)-1) +'.txt' )
                    
                    self.adicionarIO()

                    self._pages1.append(self.nome1 + '_saida_' + str(len(self._pages1)) +'.txt')

                    arq_saida_pagina = Pagina()
                    arq_saida_pagina.adicionar_tupla(tupla1parametro)

                    self._tabela1.serializador(arq_saida_pagina, self.nome1 + '_saida_' + str(len(self._pages1)-1) +'.txt' )
                    self.adicionarIO()
                else:
                    #Escreve a página de Saída para poder ser fechada para abrir a páginda de saída2(Isto é feito para respeitar
                    # o limite de 3 páginas)
                    self._tabela1.serializador(arq_saida_pagina, self.nome1 + '_saida_' + str(len(self._pages1)-1) +'.txt' )
                    self.adicionarIO()

                #Carrega a página de saída 2.Isto faz que a página de saída 1 seja "fechada"
                arq_saida_pagina = self._tabela2.deserializador(self.nome2 + '_saida_' + str(len(self._pages2)-1) +'.txt')
                if(not arq_saida_pagina.adicionar_tupla(tupla2parametroSaida)):
                    #Escreve a página de Saída Aberta e Escreve uma nova para ser usada
                    self._tabela2.serializador(arq_saida_pagina, self.nome2 + '_saida_' + str(len(self._pages2)-1) +'.txt' )
                    self.adicionarIO
                    self._pages2.append(self.nome2 + '_saida_' + str(len(self._pages2)) +'.txt')

                    arq_saida_pagina = Pagina()
                    arq_saida_pagina.adicionar_tupla(tupla2parametroSaida)

                    self._tabela2.serializador(arq_saida_pagina, self.nome2 + '_saida_' + str(len(self._pages2)-1) +'.txt' )
                    self.adicionarIO()
                else:
                    self._tabela2.serializador(arq_saida_pagina, self.nome2 + '_saida_' + str(len(self._pages2)-1) +'.txt' )
                    self.adicionarIO()

    def juncao(self, diretorio1, diretorio2, coluna1, coluna2, pg1, pg2):
        pagina1 = Pagina()
        self.adicionarIO()

        #Estão sendo criadas páginas vazias para a saída para deixar padrao(Não sei se contaria como IO)
        self._pages1.append(self.nome1+ '_saida_0.txt')
        self._pages2.append(self.nome2+ '_saida_0.txt')
        self._tabela1.serializador(pagina1, self._pages1[0])
        self._tabela2.serializador(pagina1, self._pages2[0])

        #Estamos pegando apenas os valores distintos do diretorio 1(Caso haja diretorio duplicado com
        # vários buckets que não precisaram ser divididos ainda)
        diretorio1Passado = list(dict.fromkeys(diretorio1))
        
        #Laço para ler todos os buckets
        for nomeTab1 in diretorio1Passado:
            
            arq1 = open(self.nome1+ '_' +nomeTab1 + '.txt', 'r')
            
            #Lendo a quantidade de registros para fazer o laço abaixo
            pl_reg1 = arq1.readline().split(',')
            qtdRegistros1 = int(pl_reg1[1][:-1])

            #Aqui é o passo de passar por cada tupla da tabela1 e acessar a partição correspondente
            #de uma tupla da tabela2 para fazer se satisfaz a igualdade 
            for i in range(qtdRegistros1):
                registro1 = arq1.readline().split(',')
                registro1[len(registro1)-1] = registro1[len(registro1)-1][:-1]
                registro1 = ','.join(registro1)
                
                tupla1 = Tupla()
                tupla1.adicionar_atributo(registro1)

                #Usado para carregar toda uma página
                if(not pagina1.adicionar_tupla(tupla1)):
                    #Quando a partição do bucket estiver cheia, então passa pelas tuplas dessa página
                    for tupla in pagina1.tuplas:
                        chave = int(tupla[coluna1])
                        #Função para acessar a partição correspondente na tabela2
                        self.aplicarhashTab2(tupla, chave ,diretorio2, pg2, coluna2)

                        self.adicionarIO()
                        #Como passa para a próxima tupla, deve ser adicionado um IO
                    #Carrega a próxima página(Partição do bucket)
                    pagina1 = Pagina()
                    pagina1.adicionar_tupla(tupla1)
            #Caso a última página não esteja cheia,não irá entrar no if acima.Emtão,é necessário 
            # ter o laço abaixo para ler as tuplas desta página incompleta(caso haja)
            for tupla in pagina1.tuplas:
                chave = int(tupla[coluna1])
                self.aplicarhashTab2(tupla, chave ,diretorio2, pg2, coluna2)


    def executar(self):
        #Pega o  indice da coluna que será usado como chave para a indexação hash
        coluna1 = self._tabela1.esquema.nome_para_indice[self.colTab1]

        #Caso seja pais_id, deve passar que o tam máximo do bucket é 200 para não cair no problema
        #discutido em sala
        if self.colTab1 == 'pais_producao_id' or self.colTab1 == 'pais_id' or self.colTab1 == 'pais_origem_id':
            tamMaximo = 200
        else:
            tamMaximo = 32
        #Realiza a indexação hash da tabela 1
        self.adicionarNIOs(hash(self._tabela1, coluna1 , self.nome1 + '_', tamMaximo))

        coluna2 = self._tabela2.esquema.nome_para_indice[self.colTab2]
        if self.colTab2 == 'pais_producao_id' or self.colTab2 == 'pais_id' or self.colTab2 == 'pais_origem_id':
            tamMaximo = 200
        else:
            tamMaximo = 32
        self.adicionarNIOs(hash(self._tabela2, coluna2 , self.nome2 + '_', tamMaximo))

        #Os diretórios são carregados para serem percorridos
        diretorio1 = []
        diretorio1,pg1 = self.carregarDiretorio(diretorio1,self.nome1 + '_')
        
        diretorio2 = []
        diretorio2,pg2 = self.carregarDiretorio(diretorio2,self.nome2 + '_')

        #A operação de juncao é feita
        self.juncao(diretorio1, diretorio2, coluna1, coluna2, pg1, pg2)
    
    def salvarTuplasGeradas(self, nomeArquivoSaida):
        saida = open(nomeArquivoSaida, 'w', newline='', encoding='utf-8')
        w = csv.writer(saida)

        #Seção para gravar o nome das colunas do csv
        saidaLinha = []
        for chave in self._tabela1.esquema.nome_para_indice.keys():
            saidaLinha.append(chave)
        for chave in self._tabela2.esquema.nome_para_indice.keys():
            saidaLinha.append(chave)
        w.writerow(saidaLinha)
        saidaLinha = []

        #Lê cada dupla de página de saídas para gravar no csv de saída(então, respeita as 3 páginas)
        for i in range(len(self._pages1)):
            Pagina1 = self._tabela1.deserializador(self._pages1[i])
            Pagina2 = self._tabela1.deserializador(self._pages2[i])
            
            tuplas1 = Pagina1.tuplas
            tuplas2 = Pagina2.tuplas

            for j in range(len(tuplas1)):
                saidaLinha.append(tuplas1[j]+ tuplas2[j])
        w.writerows(saidaLinha)

    #Função só para excluir os arquivos da operação testada para que se possa fazer a correção dos arquivos
    #de uma próxima operação de maneira mais fácil
    def excluirParaCorrecao(self, vinho, uva, pais):
        diretorio1 = []
        diretorio1,pg1 = self.carregarDiretorio(diretorio1,self.nome1 + '_')
        diretorio1Passado = list(dict.fromkeys(diretorio1))
        for arquivo in diretorio1Passado:
            remove(self.nome1 + '_' + arquivo + '.txt')
        remove(self.nome1 + '_diretorio.txt')
        diretorio2 = []
        diretorio2,pg2 = self.carregarDiretorio(diretorio2,self.nome2 + '_')

        diretorio2Passado = list(dict.fromkeys(diretorio2))
        for arquivo in diretorio2Passado:
            remove(self.nome2 + '_' + arquivo + '.txt')
        remove(self.nome2 + '_diretorio.txt')

        for arquivo in self._pages1:
            remove(arquivo)
        for arquivo in self._pages2:
            remove(arquivo)
        
        for arquivo in vinho.pages:
            remove(arquivo)
        remove('vinho_tabela.txt')

        for arquivo in uva.pages:
            remove(arquivo)
        remove('uva_tabela.txt')

        for arquivo in pais.pages:
            remove(arquivo)
        remove('pais_tabela.txt')
