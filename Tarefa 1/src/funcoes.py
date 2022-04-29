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
def buscarBucket(chave_busca,bucket,diretorio):
    dados_bucket = []
    #Carrega o bucket para memória principal
    with open(diretorio[bucket] + '.txt','r') as dados:
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


def inserir(id_vinho,chave_busca,bucket,diretorio):
    #Pega a profundidade global atual do diretorio
    profundidadeGlobal = log2(len(diretorio))
    
    #Carrega o bucket em que será feita a inserção para a memória principal
    with open(diretorio[bucket] + '.txt','r') as arq:
        pl_reg =arq.readline() 
        pl_reg= pl_reg.split(',') #[0] = pl ; [1] = qntd registro     
        #Variável com as entradas de dados daquele bucket
        registros = arq.readlines()

    #Verifica se o número de registros daquele bucket é menor que 32,pois,
    # caso seja 32(capacidade de uma página),será necessário duplicar o diretório ou dividir o bucket 
    if(int(pl_reg[1][:-1])<32):
        #Passo para somar um a quantidade de registros no conteudo da linha
        quantidade_registros = pl_reg[1][:-1]
        quantidade_registros = int(quantidade_registros) +1
        pl_reg[1] = str(quantidade_registros)

        with tempfile.NamedTemporaryFile('w', delete=False) as out:
            out.write(f"{pl_reg[0]},{pl_reg[1]}\n")
            for registro in registros:
                out.write(registro)
            out.write(f"{id_vinho},{chave_busca}\n")
        shutil.move(out.name, diretorio[bucket] + '.txt')
    #Caso a profundidade local daquele bucket cheio seja maior ou igual a global, é necessário duplicar o
    #diretório
    elif int(pl_reg[0])>=profundidadeGlobal:
        #
        duplicarDiretorio(diretorio,bucket)
        
        profundidadeGlobal+=1
        if(int(len(diretorio)//2)<=bucket):
            divisaoBucket(bucket, bucket - len(diretorio)//2, diretorio, True)  
        else:
            divisaoBucket(bucket, bucket + len(diretorio)//2, diretorio, True)
        inserir(id_vinho,chave_busca,mascara(int(chave_busca),len(diretorio[bucket])),diretorio)
    #Caso não seja, basta fazer a divisão do bucket
    else:
        """
        Neste teste quero ver o seguinte:
        Considere o diretorio ['00', '001', '10', '11', '00', '101', '10', '11']
        Quero ver, por exemplo, se é o 10 da posição 2 ou da posição 6 para informar
        a função de divisão"""
        if(int(len(diretorio)/2)<=bucket):
            divisaoBucket(bucket,bucket-int(len(diretorio)//2),diretorio)
        else:
            divisaoBucket(bucket,bucket+int(len(diretorio)//2),diretorio)
        
    return int(profundidadeGlobal)


def duplicarDiretorio(diretorio,bucket):

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

    with open(diretorio[bucket]+'.txt','r') as arq:
        pl_reg =arq.readlines()

    with open(diretorio[bucket]+'.txt','w') as arq:
        arq.write(f"{pl+1},{pl_reg[0].split(',')[1]}")
        for registro in pl_reg[1:]:
            arq.write(registro)

    if(int(len(diretorio)//2)<=bucket):
        shutil.move(diretorio[bucket] + '.txt','1' + diretorio[bucket] + '.txt')
   
        diretorio[bucket] = '1' + diretorio[bucket] 
    else:
        shutil.move(diretorio[bucket] + '.txt','0' + diretorio[bucket] + '.txt')
   
        diretorio[bucket] = '0' + diretorio[bucket] 
    
    #Criando o novo bucket para o bucket correspondente que disparou a duplicacao de diretorio
    if(int(len(diretorio)/2)>=bucket):
        with open(diretorio[bucket-tamanho_anterior]+'.txt','w') as bucketNovo:
            bucketNovo.write(f"{pl+1},0\n")
    else:
        with open(diretorio[bucket+tamanho_anterior]+'.txt','w') as bucketNovo:
            bucketNovo.write(f"{pl+1},0\n")
    

def divisaoBucket(bucketAntigo,bucketNovo,diretorio, diretorioDuplicado = False):
    pl = len(diretorio[bucketAntigo])
    
    #Isto é o equivalente a carregar o bucket para a memória principal para que se possa fazer a divisao
    with open(diretorio[bucketAntigo] + '.txt','r') as arq:
        registros = arq.readlines()[1:]
    
    #Verifica se a operação foi chamada após a duplicação do diretorio
    if(diretorioDuplicado):
        arq1 = open(diretorio[bucketAntigo] + '.txt','w')
        arq2 = open(diretorio[bucketNovo] + '.txt','w')

        arq1.write(f"{pl},0\n")
        arq2.write(f"{pl},0\n")

        arq1.close()
        arq2.close()
    else:
        #Neste trecho um novo bucket é criado e o outro bucket é renomeado conforme os parametros
        arq1 = open(diretorio[bucketAntigo] + '.txt','w')
        arq1.write(f"{int(pl) + 1},0\n")
        arq1.close()

        if(int(len(diretorio)/2)<=bucketAntigo):
            shutil.move(diretorio[bucketAntigo]+'.txt', '1'+diretorio[bucketAntigo]+'.txt')
            diretorio[bucketAntigo] = '1' + diretorio[bucketAntigo]

            diretorio[bucketNovo] = '0' + diretorio[bucketNovo]
            with open(diretorio[bucketNovo]+'.txt','w') as arq:
                arq.write(f"{pl+1},0\n")
        else:
            shutil.move(diretorio[bucketAntigo]+'.txt', '0'+diretorio[bucketAntigo]+'.txt')
            diretorio[bucketNovo] = '1' + diretorio[bucketNovo]

            diretorio[bucketAntigo] = '0' + diretorio[bucketAntigo]
            with open(diretorio[bucketNovo]+'.txt','w') as arq:
                arq.write(f"{pl+1},0\n")
    #Insere entrada a entrada no bucket correto
    for registro in registros:
       
        dados = registro.split(',')
        chave = int(dados[1][:-1])
        
        if(diretorioDuplicado):
            enderecoDiretorio = mascara(chave, pl)
        else:
            enderecoDiretorio = mascara(chave, pl+1)
        if(diretorio[enderecoDiretorio]==diretorio[bucketAntigo]):
            inserir(dados[0], chave,bucketAntigo, diretorio)
        else:
            inserir(dados[0], chave, bucketNovo, diretorio)


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


def remover(diretorio,chave_busca):
    tam_diretorio = len(diretorio)
    pg = int(log2(tam_diretorio))

    indice_bucket = mascara(chave_busca, pg)
    registros_atuais =removerBucket(diretorio[indice_bucket]+".txt",chave_busca)
    #indice_balde_amigo = str(int(not(int(diretorio[indice_bucket][0]))))+diretorio[indice_bucket][1:]
    
    #Verificando se há como diminuir o diretório
    if(len(diretorio[indice_bucket])==pg):
        #Primeiramente verifica-se se há balde amigo comparando a profundidade local com a global
        if((tam_diretorio//2)<=indice_bucket):
            indice_bucket_amigo = indice_bucket - tam_diretorio//2
        else:
            indice_bucket_amigo = indice_bucket + tam_diretorio//2

        #Agora, deve-se verificar se um bucket consegue comportar as entradas dos dois.
        with open(diretorio[indice_bucket_amigo]+'.txt', 'r') as arq:
            registrosBucketAmigo = int(arq.readline().split(',')[1][:-1] )

        if(registros_atuais[1]+registrosBucketAmigo<=32 and pg>2):
            #Se passa por este teste, então um bucket consegue comportar as entradas
            #Agora, deve-se verificar se todos os buckets da segunda metade do diretório tem profundidade
            #local menor que a global
            quantidade_teste = 0
            for i in range(tam_diretorio//2,tam_diretorio):
                
                if(len(diretorio[i]))>=pg:
                    quantidade_teste += 1
            if(quantidade_teste==1):
                #Significa que só há um bucket com pg==pl, logo o diretório pode ser reduzido
                FundirBucket(indice_bucket,indice_bucket_amigo,diretorio,True)
            else:
                #Significa que há mais de um bucket com pg==pl, então só pode fundir os buckets
                FundirBucket(indice_bucket,indice_bucket_amigo,diretorio)
    return registros_atuais[0] - registros_atuais[1]        


def FundirBucket(indice_bucket, indice_bucket_amigo, diretorio, reduzirDiretorio = False):
    
    #Verifica qual o bucket amigo
    if(indice_bucket<indice_bucket_amigo):
        indiceUsado = indice_bucket
        indiceRemovido = indice_bucket_amigo
    else:
        indiceUsado = indice_bucket_amigo
        indiceRemovido = indice_bucket
    
    #Aqui os arquivos são abertos para carregar os buckets para a memória principal
    with open(diretorio[indiceUsado]+'.txt','r') as arq1, open(diretorio[indiceRemovido]+'.txt','r') as arq2:
        pl_reg = arq1.readline().split(',')
        profundidadeLocal = int(pl_reg[0])
        quantRegistros1 = int(pl_reg[1][:-1])

        registros1 = arq1.readlines()


        quantRegistros2 = int(arq2.readline().split(',')[1][:-1])
    
        registros2 = arq2.readlines()
    
    #Coloca todas as entradas no bucket que sobrará
    with open(diretorio[indiceUsado]+'.txt', 'w') as arq:
        arq.write(f"{profundidadeLocal-1},{quantRegistros1+quantRegistros2}\n")

        for registro in registros1:
            arq.write(registro)
        
        for registro in registros2:
            arq.write(registro)
    #Renomea o arquivo do bucket que permanecerá
    shutil.move(diretorio[indiceUsado]+'.txt', diretorio[indiceUsado][1:]+'.txt')

    #Remove o bucket que não será mais usado
    remove('./'+diretorio[indiceRemovido] +'.txt')
    #Corrige os nomes dos arquivos em binario no diretorio
    diretorio[indiceUsado] = diretorio[indiceUsado][1:]
    diretorio[indiceRemovido] = diretorio[indiceRemovido][1:]
    
    tamDiretorio = len(diretorio)
    #Se for necessário reduzir o diretorio,exclui os indices da segunda metade 
    if(reduzirDiretorio):
        for registro in diretorio[tamDiretorio//2:]:
            diretorio.remove(registro)

