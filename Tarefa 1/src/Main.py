from math import log2
import funcoes


"""
Explicando a estratégia utilizada para o diretorio e o acesso aos buckets:
O diretorio carregado em memória principal será uma lista de strings, onde cada string
armazenará o nome binário sem a extensão .txt.Por exemplo:
diretorio = ['00', '01', '10', '11']
Neste diretorio de profundidade global 2,são salvos os nomes dos arquivos que correspondem aos binários
dos n últimos bits de um número,em que n é a profundidade global do bucket.

Por que fazemos isso?
Note que, caso a chave de busca seja 2007, sua representação binária é 11111010111.Considerando que a profundidade
global do diretorio definido acima é 2, então pegamos 11.
11 é 3 em base 10 e essa é justamente a posição no diretorio em que o nome do arquivo(arquivo em que as operações com 2007 devem ser feitas)

E se tivermos o diretorio duplicado?

diretorio2 = ['00', '001', '10', '11', '00', '101', '10', '11']

Caso a chave de busca seja 2010,sua representação binária é 11111011010.Considerando que a profundidade
global do diretorio2 definido acima é 3, então pegamos 010.

010 é 2 em base 10.Daí, o nome do arquivo na posição 2 do diretorio é 10.Como este bucket ainda não foi duplicado,
acessamos o arquivo certo.

Por fim, podemos concluir que esta estratégia foi adotada para que o nome dos diretorios possam ser acessados de forma
fácil apenas pegando a posição considerando o valor em base 10 nos n últimos bits da chave. 
"""

"""
Aviso: O [:-1] usado muitas vezes ao longo deste código serve para retirar a quebra de linha no final da string """

#Abre o arquivo in.txt em modo de leitura e o out.txt(Arquivo que será escrito conforme a especificação) em modo de escrita
with open("in.txt",'r') as entrada, open("out.txt",'w') as saida:
    #Carrega todas as linhas do arquivo in.txt para saber quais comandos serão executados
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

    #Carrega os registros de vinhos.csv para a memória principal
    with open('vinhos.csv','r') as base_dados:
        dados = base_dados.readlines()[1:]
        
    for i in range(len(dados)):
        #Separa os valores de cada coluna de uma linha para que os valores necesssários sejam pegues facilmente
        dados[i]= dados[i].split(",")
    for op in comandos:
        operacao = op
        operacao =operacao.split(':')
        if operacao[0][:3]== "INC":
            chave = operacao[1][:-1]
            
            #Variável para contar quantos registros com determinada chave foram inseridos
            qtdTuplasInseridas = 0
            
            for i in dados:
                #Percorre os registros e insere os que apresentam a chave de busca igual a passada
                if(i[2] == chave):  
                    profundidadeGlobal = funcoes.inserir(i[0], int(i[2]), funcoes.mascara(int(chave), profundidadeGlobal),diretorioEntradas)
                    qtdTuplasInseridas+=1
            saida.write(f"INC:{chave}/{qtdTuplasInseridas}\n")
            
        elif operacao[0][:3]== "REM":
            chave = operacao[1][:-1]
            #qtdRegistrosRemov armazena a quantidade de registros removidos
            qtdRegistrosRemov = funcoes.remover(diretorioEntradas,int(chave))
            
            #Pega a profundidade global atual para atualizar após a remoção
            profundidadeGlobal = int(log2(len(diretorioEntradas)))
            
            #Na especificação, entendemos que é gravado no out.txt a profundidade global de quando a operação foi feita
            # e a profundidade local do bucket em que estava o registro(ou bucket amigo em um caso da fusão de buckets)
            # após a remoção 
            saida.write(f"REM:{chave}/{qtdRegistrosRemov},{profundidadeGlobal},{len(diretorioEntradas[int(funcoes.mascara(int(chave),profundidadeGlobal) ) ] )}\n")
        elif operacao[0][:3]== "BUS" and operacao[0][3] =='=':
            #Fazer busca
            chave_busca = int(operacao[1][:-1])
            #A variável tuplas armazena todas as tuplas buscadas
            tuplas = funcoes.buscarBucket(chave_busca, funcoes.mascara(chave_busca,profundidadeGlobal), diretorioEntradas)
            #Caso queira ver as tuplas no console, basta descomentar o trecho abaixo
            """
            print(f"Busca das tuplas de chave {chave_busca}")
            for tupla in tuplas:
                print(tupla)
            """

            #Grava em out.txt conforme a especificação
            saida.write(f"BUS:{chave_busca}/{len(tuplas)}\n")
        else:
            pass
    
    #Abre em modo de escrita para salvar o diretorio após as operações especificadas em in.txt
    with open('diretorio.txt','w') as diretorioSaida:
        diretorioSaida.write(f"{profundidadeGlobal}\n")

        for enderecoDiretorioSaida in diretorioEntradas:
            diretorioSaida.write(f"{enderecoDiretorioSaida}\n")
