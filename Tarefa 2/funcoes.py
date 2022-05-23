import  shutil, tempfile
from math import log2
from os import remove


""" 
Mascara de bits
Retorna os exatos b ultimos bits de um inteiro
""" 
def mascara(inteiro, b):
    mask = 2**(b)-1
    return inteiro & mask


"""
Busca no bucket(acessa o arquivo corretamente conforme explicado em Main.py) pelas entradas com a chave
de busca passada.
O seu parametro bucket é a posição em que uma entrada com aquela chave de busca estará no diretorio"""
def buscarBucket(chave_busca,bucket,diretorio, prefixo):
    dados_bucket = []
    #Carrega o bucket para memória principal
    with open(prefixo + diretorio[bucket] + '.txt','r') as dados:
        dados.readline()
        eof = False
        
        while(not (eof)):
            linha = dados.readline()
            if linha=='':
                eof=True
            elif int(linha.split(',')[1])== chave_busca:
              dados_bucket.append(linha[:-1])
    #Retorna as tuplas com aquela chave de busca    
    return dados_bucket


def inserir(tupla,coluna,bucket,diretorio, prefixo, tamMaximo):
    #Pega a profundidade global atual do diretorio
    profundidadeGlobal = log2(len(diretorio))
    chave_busca = int(tupla[coluna])
    
    #Carrega o bucket em que será feita a inserção para a memória principal
    with open(prefixo + diretorio[bucket] + '.txt','r') as arq:
        pl_reg =arq.readline() 
        pl_reg= pl_reg.split(',') #[0] = pl ; [1] = qntd registro     
        #Variável com as entradas de dados daquele bucket
        registros = arq.readlines()

    #Verifica se o número de registros daquele bucket é menor que 32,pois,
    # caso seja 32(capacidade de uma página),será necessário duplicar o diretório ou dividir o bucket 
    if(int(pl_reg[1][:-1])<tamMaximo):
        #Passo para somar um a quantidade de registros no conteudo da linha
        quantidade_registros = pl_reg[1][:-1]
        quantidade_registros = int(quantidade_registros) +1
        pl_reg[1] = str(quantidade_registros)

        with tempfile.NamedTemporaryFile('w', delete=False) as out:
            out.write(f"{pl_reg[0]},{pl_reg[1]}\n")
            for registro in registros:
                out.write(registro)
            out.write(f"{','.join(tupla)}\n")
        shutil.move(out.name,prefixo + diretorio[bucket] + '.txt')
    #Caso a profundidade local daquele bucket cheio seja maior ou igual a global, é necessário duplicar o
    #diretório
    elif int(pl_reg[0])>=profundidadeGlobal:

        duplicarDiretorio(diretorio,bucket, prefixo, tamMaximo)
        
        profundidadeGlobal+=1
        if(int(len(diretorio)//2)<=bucket):
            divisaoBucket(bucket, bucket - len(diretorio)//2, diretorio, prefixo, tamMaximo, coluna ,True)  
        else:
            divisaoBucket(bucket, bucket + len(diretorio)//2, diretorio, prefixo,tamMaximo,coluna ,True)
        inserir(tupla,coluna,mascara(int(chave_busca),len(diretorio[bucket])),diretorio, prefixo, tamMaximo)
    #Caso não seja, basta fazer a divisão do bucket
    else:
        """
        Neste teste quero ver o seguinte:
        Considere o diretorio ['00', '001', '10', '11', '00', '101', '10', '11']
        Quero ver, por exemplo, se é o 10 da posição 2 ou da posição 6 para informar
        a função de divisão"""
        if(int(len(diretorio)/2)<=bucket):
            divisaoBucket(bucket,bucket-int(len(diretorio)//2),diretorio, prefixo,tamMaximo, coluna)
        else:
            divisaoBucket(bucket,bucket+int(len(diretorio)//2),diretorio, prefixo, tamMaximo, coluna)
        inserir(tupla,coluna,mascara(int(chave_busca),len(diretorio[bucket])),diretorio, prefixo, tamMaximo)
    
    return int(profundidadeGlobal)


def duplicarDiretorio(diretorio, bucket, prefixo, tamMaximo):

    tamanho_anterior= len(diretorio)
    pl = len(diretorio[bucket])
    #Adiciona os mesmos indices
    for i in range(tamanho_anterior):
        diretorio.append(diretorio[i])

    #Corrige o nome no diretorio no indice do bucket que disparou a dupliacação(Pois apenas
    # ele precisa ser dividido no momento)
    if(int(len(diretorio)/2)<=bucket):
        diretorio[bucket-tamanho_anterior] = '0' + diretorio[bucket]
    else:
        diretorio[bucket+tamanho_anterior] = '1' + diretorio[bucket]

    with open(prefixo + diretorio[bucket]+'.txt','r') as arq:
        pl_reg =arq.readlines()

    with open(prefixo + diretorio[bucket]+'.txt','w') as arq:
        arq.write(f"{pl+1},{pl_reg[0].split(',')[1]}")
        for registro in pl_reg[1:]:
            arq.write(registro)

    if(int(len(diretorio)//2)<=bucket):
        shutil.move(prefixo + diretorio[bucket] + '.txt',prefixo + '1' + diretorio[bucket] + '.txt')
   
        diretorio[bucket] = '1' + diretorio[bucket] 
    else:
        shutil.move(prefixo + diretorio[bucket] + '.txt',prefixo + '0' + diretorio[bucket] + '.txt')
   
        diretorio[bucket] = '0' + diretorio[bucket] 
    
    #Criando o novo bucket para o bucket correspondente que disparou a duplicacao de diretorio
    if(int(len(diretorio)/2)>=bucket):
        with open(prefixo + diretorio[bucket-tamanho_anterior]+'.txt','w') as bucketNovo:
            bucketNovo.write(f"{pl+1},0\n")
    else:
        with open(prefixo + diretorio[bucket+tamanho_anterior]+'.txt','w') as bucketNovo:
            bucketNovo.write(f"{pl+1},0\n")
    

def divisaoBucket(bucketAntigo,bucketNovo,diretorio, prefixo,tamMaximo, coluna ,diretorioDuplicado = False):
    pl = len(diretorio[bucketAntigo])
    
    #Isto é o equivalente a carregar o bucket para a memória principal para que se possa fazer a divisao
    with open(prefixo + diretorio[bucketAntigo] + '.txt','r') as arq:
        registros = arq.readlines()[1:]
    
    #Verifica se a operação foi chamada após a duplicação do diretorio
    if(diretorioDuplicado):
        arq1 = open(prefixo + diretorio[bucketAntigo] + '.txt','w')
        arq2 = open(prefixo + diretorio[bucketNovo] + '.txt','w')

        arq1.write(f"{pl},0\n")
        arq2.write(f"{pl},0\n")

        arq1.close()
        arq2.close()
    else:
        #Neste trecho um novo bucket é criado e o outro bucket é renomeado conforme os parametros
        arq1 = open(prefixo + diretorio[bucketAntigo] + '.txt','w')
        arq1.write(f"{int(pl) + 1},0\n")
        arq1.close()

        valorMudanca = diretorio[bucketAntigo]
        contadorTroca = diretorio.count(valorMudanca)

        if(int(len(diretorio)/2)<=bucketAntigo):
            shutil.move(prefixo + diretorio[bucketAntigo]+'.txt', prefixo + '1'+diretorio[bucketAntigo]+'.txt')
            """diretorio[bucketAntigo] = '1' + diretorio[bucketAntigo]
            
            diretorio[bucketNovo] = '0' + diretorio[bucketNovo]
            Aqui está comentado o código antigo.
            Qual era o problema?
            Basicamente quando um bucket precisava ser dividido e sua profundidade local
            era pl<=pg-2 , havia o problema de não atualizar todas as suas referências no diretório.
            Por exemplo:
            [00,0001,10,11,00,0101,10,11,00,1001,10,11,00,1101,10,11]
            Digamos que 0101 causasse outra duplicação de diretório:
            [00,0001,10,11,00,00101,10,11,00,1001,10,11,00,1101,10,11,00,0001,10,11,00,10101,10,11,00,1001,10,00,11,1101,10,11]
            Após a duplicação, caso o 00 precise ser divido, o que o código fazia anteriormente era apenas orrigir duas
            referências de 00(uma à esquerda e outra à direita), mas há 8, então claramente daria problema no hash.
            """

            for i in range(contadorTroca):
                posicaoMudanca = diretorio.index(valorMudanca)
                if(len(diretorio)/2<posicaoMudanca):
                    diretorio[posicaoMudanca] = '1' + diretorio[posicaoMudanca]
                else:
                    diretorio[posicaoMudanca] = '0' + diretorio[posicaoMudanca]
            with open(prefixo + diretorio[bucketNovo]+'.txt','w') as arq:
                arq.write(f"{pl+1},0\n")
        else:
            shutil.move(prefixo + diretorio[bucketAntigo]+'.txt', prefixo + '0'+diretorio[bucketAntigo]+'.txt')
            """diretorio[bucketNovo] = '1' + diretorio[bucketNovo]

            diretorio[bucketAntigo] = '0' + diretorio[bucketAntigo]
            Aqui está comentado o código antigo.
            A explicação do problema que estava dando está acima
            """
            for i in range(contadorTroca):
                posicaoMudanca = diretorio.index(valorMudanca)
                if(len(diretorio)/2<posicaoMudanca):
                    diretorio[posicaoMudanca] = '1' + diretorio[posicaoMudanca]
                else:
                    diretorio[posicaoMudanca] = '0' + diretorio[posicaoMudanca]
            with open(prefixo + diretorio[bucketNovo]+'.txt','w') as arq:
                arq.write(f"{pl+1},0\n")
    
    #Insere entrada a entrada no bucket correto
    for registro in registros:
       
        dados = registro.split(',')
        dados[len(dados)-1] = dados[len(dados)-1][:-1]
        chave = int(dados[coluna])

        if(diretorioDuplicado):
            enderecoDiretorio = mascara(chave, pl)
        else:
            enderecoDiretorio = mascara(chave, pl+1)
        if(diretorio[enderecoDiretorio]==diretorio[bucketAntigo]):
            inserir(dados,coluna,bucketAntigo, diretorio, prefixo, tamMaximo)
        else:
            inserir(dados, coluna, bucketNovo, diretorio, prefixo, tamMaximo)


def removerBucket(indice_bucket,chave):
    with open(indice_bucket,'r') as bucket:
        tuplas = bucket.readlines()
    pl= tuplas[0].split(",")[0]
    #Como o primeiro elemento de tuplas são as informações do bucket ,subtrai um abaixo
    tam_original = len(tuplas) - 1
    for tupla in tuplas[1:]:
        if(tupla.split(",")[1][:-1] == str(chave)):
            tuplas.remove(tupla)

    with open(indice_bucket,"w") as bucket_alterado:
        tuplas[0] =f"{pl},{len(tuplas)-1}\n"
        
        for i in tuplas:
            bucket_alterado.write(i)
            
    return (tam_original,len(tuplas)-1)


#A partir daqui o trabalho anterior não foi adaptado
def remover(diretorio, chave_busca, prefixo):
    tam_diretorio = len(diretorio)
    pg = int(log2(tam_diretorio))

    indice_bucket = mascara(chave_busca, pg)
    registros_atuais =removerBucket(prefixo + diretorio[indice_bucket]+".txt",chave_busca)
    #indice_balde_amigo = str(int(not(int(diretorio[indice_bucket][0]))))+diretorio[indice_bucket][1:]
    
    #Verificando se há como diminuir o diretório
    if(len(diretorio[indice_bucket])==pg):
        #Primeiramente verifica-se se há balde amigo comparando a profundidade local com a global
        if((tam_diretorio//2)<=indice_bucket):
            indice_bucket_amigo = indice_bucket - tam_diretorio//2
        else:
            indice_bucket_amigo = indice_bucket + tam_diretorio//2

        #Agora, deve-se verificar se um bucket consegue comportar as entradas dos dois.
        with open(prefixo + diretorio[indice_bucket_amigo]+'.txt', 'r') as arq:
            registrosBucketAmigo = int(arq.readline().split(',')[1][:-1] )

        if(registros_atuais[1]+registrosBucketAmigo<=12 and pg>2):
            #Se passa por este teste, então um bucket consegue comportar as entradas
            #Agora, deve-se verificar se todos os buckets da segunda metade do diretório tem profundidade
            #local menor que a global
            quantidade_teste = 0
            for i in range(tam_diretorio//2,tam_diretorio):
                
                if(len(diretorio[i]))>=pg:
                    quantidade_teste += 1
            if(quantidade_teste==1):
                #Significa que só há um bucket com pg==pl, logo o diretório pode ser reduzido
                FundirBucket(indice_bucket,indice_bucket_amigo,diretorio, prefixo, True)
            else:
                #Significa que há mais de um bucket com pg==pl, então só pode fundir os buckets
                FundirBucket(indice_bucket,indice_bucket_amigo,diretorio, prefixo)
    return registros_atuais[0] - registros_atuais[1]        


def FundirBucket(indice_bucket, indice_bucket_amigo, diretorio, prefixo, reduzirDiretorio = False):
    
    #Verifica qual o bucket amigo
    if(indice_bucket<indice_bucket_amigo):
        indiceUsado = indice_bucket
        indiceRemovido = indice_bucket_amigo
    else:
        indiceUsado = indice_bucket_amigo
        indiceRemovido = indice_bucket
    
    #Aqui os arquivos são abertos para carregar os buckets para a memória principal
    with open(prefixo + diretorio[indiceUsado]+'.txt','r') as arq1, open(prefixo + diretorio[indiceRemovido]+'.txt','r') as arq2:
        pl_reg = arq1.readline().split(',')
        profundidadeLocal = int(pl_reg[0])
        quantRegistros1 = int(pl_reg[1][:-1])

        registros1 = arq1.readlines()


        quantRegistros2 = int(arq2.readline().split(',')[1][:-1])
    
        registros2 = arq2.readlines()
    
    #Coloca todas as entradas no bucket que sobrará
    with open(prefixo + diretorio[indiceUsado]+'.txt', 'w') as arq:
        arq.write(f"{profundidadeLocal-1},{quantRegistros1+quantRegistros2}\n")

        for registro in registros1:
            arq.write(registro)
        
        for registro in registros2:
            arq.write(registro)
    #Renomea o arquivo do bucket que permanecerá
    shutil.move(prefixo + diretorio[indiceUsado]+'.txt', prefixo + diretorio[indiceUsado][1:]+'.txt')

    #Remove o bucket que não será mais usado
    remove('./'+ prefixo + diretorio[indiceRemovido] +'.txt')
    #Corrige os nomes dos arquivos em binario no diretorio
    diretorio[indiceUsado] = diretorio[indiceUsado][1:]
    diretorio[indiceRemovido] = diretorio[indiceRemovido][1:]
    
    tamDiretorio = len(diretorio)
    #Se for necessário reduzir o diretorio,exclui os indices da segunda metade 
    if(reduzirDiretorio):
        for registro in diretorio[tamDiretorio//2:]:
            diretorio.remove(registro)

