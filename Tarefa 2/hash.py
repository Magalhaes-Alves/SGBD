from math import log2
import funcoes
from Tabela import Tabela
from Pagina import Pagina
from Tupla import Tupla

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
def hash(tabela, coluna, prefixo):
    #Abre o arquivo in.txt em modo de leitura e o out.txt(Arquivo que será escrito conforme a especificação) em modo de escrita
    #Carrega todas as linhas do arquivo in.txt para saber quais comandos serão executados
    
    #Seção para carregar o diretorio para a memoria principal
    try:
        #Tenta abrir o arquivo
        diretorio = open(prefixo + "diretorio.txt","r")
        
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
            with open(prefixo + nomeBucket+'.txt','w') as arq:
                arq.write("2,0\n")

    paginas = tabela._pages

    for pagina in paginas:
        for tupla in pagina._tuplas:
            profundidadeGlobal = funcoes.inserir(tupla[coluna], int(tupla[coluna]), funcoes.mascara(int(tupla[coluna]), profundidadeGlobal),diretorioEntradas,prefixo)

        """elif operacao[0][:3]== "BUS" and operacao[0][3] =='=':
            Fazer busca
            chave_busca = int(operacao[1][:-1])
            A variável tuplas armazena todas as tuplas buscadas
            tuplas = funcoes.buscarBucket(chave_busca, funcoes.mascara(chave_busca,profundidadeGlobal), diretorioEntradas)"""

    
    #Abre em modo de escrita para salvar o diretorio após as operações especificadas em in.txt
    with open(prefixo + 'diretorio.txt','w') as diretorioSaida:
        diretorioSaida.write(f"{profundidadeGlobal}\n")

        for enderecoDiretorioSaida in diretorioEntradas:
            diretorioSaida.write(f"{enderecoDiretorioSaida}\n")
