import shutil
import funcoes



with open("in.txt",'r') as entrada, open("out.txt",'w') as saida:
    comandos = entrada.readlines()
    
    #Seção para carregar o diretorio para a memoria principal
    try:
        #Tenta abrir o arquivo
        diretorio = open("diretorio.txt","r")
        
        profundidadeGlobal =int(diretorio.readline()[:-1])
        
        diretorioEntradas = []
        eof = False
        
        #Carregando os enderecos para os buckets.Nesta aplicacao, serao os nomes dos arquivos
        while(not (eof)):
            linha = diretorio.readline()
            if linha=='':
                eof=True
            else:
                diretorioEntradas.append(linha[:-1])
    except OSError:
        #Caso não exista arquivo de diretorio, são colocados os valores iniciais estabelecidos
        profundidadeGlobal = 2
        diretorioEntradas = ['00','01','10','11']
        for nomeBucket in diretorioEntradas:
            with open(nomeBucket+'.txt','w') as arq:
                arq.write("2,0\n")


    for op in comandos:
        operacao = op
        operacao.split(':')
        if operacao[0][0:3]== "INC":
            chave = operacao[1][:-1]
            print(chave)
            with open('vinhos.csv','r') as vinhos:
                registro = vinhos.readline()
                while(not (eof)):
                    registro = vinhos.readline()
                    if registro=='':
                        eof=True
                    else:
                        dados_vinho = registro.split(',')
                        if(chave == dados_vinho[2]):
                            profundidadeGlobal = funcoes.inserir(dados_vinho[0], dados_vinho[1], diretorioEntradas[funcoes.mascara(int(chave), profundidadeGlobal)]+'.txt',diretorio)
            
        elif operacao[0][0:3]== "REM":
            chave = operacao[1][:-1]
            print(chave)
            #funcoes.remover(diretorio,chave)
            pass
        elif operacao[0][0:2]== "BUS":
            #Fazer busca
            chave_busca = int(operacao[1][:-1])
            tuplas = funcoes.buscarBucket(chave_busca, funcoes.mascara(chave_busca,profundidadeGlobal), diretorio)
        else:
            pass
