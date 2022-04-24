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

    for op in comandos:
        operacao = op
        operacao.split(':')
        if operacao[0][0:3]== "INC":
            chave = int(operacao[1])
            funcoes.mascara(chave,profundidadeGlobal)
            funcoes.inserir(80, chave, diretorioEntradas[funcoes.mascara(chave, profundidadeGlobal)]+'.txt')
            
            pass
        elif operacao[0][0:3]== "REM":
            #Fazer remoção
            pass
        elif operacao[0][0:2]== "BUS":
            #Fazer busca
            pass
        else:
            pass
