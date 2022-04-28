
""" 
Mascara de bits
Retorna os exatos b ultimos bits de um inteiro
""" 
from distutils import dir_util
import  shutil, tempfile
from math import log2
from os import remove

def mascara(inteiro, b):
    mask = 2**(b)-1
    return inteiro & mask


def funcaoHashing(chave_busca):
    return bin(chave_busca)


def buscarBucket(chave_busca,bucket,diretorio):
    dados_bucket = []
    with open(diretorio[bucket] + '.txt','r') as dados:
        dados.readline()
        eof = False
        
        while(not (eof)):
            linha = dados.readline()
            if linha=='':
                eof=True
            elif int(linha.split(',')[1])== chave_busca:
              dados_bucket.append(linha[:-1])
        
    return dados_bucket


def enderecoBucket(chave,pg):
    endereco_bucket = bin(mascara(chave,pg))[2:]

  
    if len(endereco_bucket)<pg:
        endereco_bucket = '0' + endereco_bucket
  
    return endereco_bucket


def busca(chave, diretorio, pg):
    endereco_bucket = enderecoBucket(chave,pg)
  
    return  buscarBucket(chave, endereco_bucket+'.txt')
  

def inserir(id_vinho,chave_busca,bucket,diretorio):
    profundidadeGlobal = log2(len(diretorio))
  
    with open(diretorio[bucket] + '.txt','r') as arq:
        pl_reg =arq.readline() 
        pl_reg= pl_reg.split(',') #[0] = pl ; [1] = qntd registro     
        registros = arq.readlines()
    
    if(int(pl_reg[1][:-1])<32):
        #Passo para adicionar em um a quantidade de registros no conteudo da linha
        quantidade_registros = pl_reg[1][:-1]
        quantidade_registros = int(quantidade_registros) +1
        pl_reg[1] = str(quantidade_registros)

        with tempfile.NamedTemporaryFile('w', delete=False) as out:
            out.write(f"{pl_reg[0]},{pl_reg[1]}\n")
            for registro in registros:
                out.write(registro)
            out.write(f"{id_vinho},{chave_busca}\n")
        shutil.move(out.name, diretorio[bucket] + '.txt')

    elif int(pl_reg[0])>=profundidadeGlobal:
        tam = len(diretorio)
        duplicarDiretorio(diretorio,bucket)
        profundidadeGlobal+=1
        if(int(len(diretorio)//2)>=bucket):
            divisaoBucket(bucket, bucket - tam, diretorio, True)  
        else:
            divisaoBucket(bucket, bucket + tam, diretorio, True)
        inserir(id_vinho,chave_busca,bucket,diretorio)
    else:
        if(int(len(diretorio)/2)<=bucket):
            divisaoBucket(bucket,bucket-int(len(diretorio)/2),diretorio)
        else:
            divisaoBucket(bucket,bucket+int(len(diretorio)/2),diretorio)
        
    return profundidadeGlobal

def duplicarDiretorio(diretorio,bucket):

    tamanho_anterior= len(diretorio)
    pl = len(diretorio[bucket])

    for i in range(tamanho_anterior):
        diretorio.append(diretorio[i])

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

    if(int(len(diretorio)/2)<=bucket):
        shutil.move(diretorio[bucket] + '.txt','1' + diretorio[bucket] + '.txt')
   
        diretorio[bucket] = '1' + diretorio[bucket] 
    else:
        shutil.move(diretorio[bucket] + '.txt','0' + diretorio[bucket] + '.txt')
   
        diretorio[bucket] = '0' + diretorio[bucket] 
    
    print("Teste duplicar")
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

    with open(diretorio[bucketAntigo] + '.txt','w') as arq1,open(diretorio[bucketNovo] + '.txt','w') as arq2 :
        if(diretorioDuplicado):
            arq1.write(f"{pl},0\n")
            arq2.write(f"{pl},0\n")
        else:
            arq1.write(f"{int(pl) + 1},0\n")
            if(int(len(diretorio)/2)<=bucketAntigo):
                shutil.move(diretorio[bucketAntigo]+'.txt', '1'+diretorio[bucketAntigo]+'.txt')
                diretorio[bucketAntigo] = '1' + diretorio[bucketAntigo]

                diretorio[bucketNovo] = '0' + diretorio[bucketNovo]
                with open(diretorio[bucketNovo]+'.txt','w') as arq:
                    arq.write(f"{pl+1},0\n")
            else:
                shutil.move(diretorio[bucketNovo]+'.txt', '1'+diretorio[bucketNovo]+'.txt')
                diretorio[bucketNovo] = '1' + diretorio[bucketNovo]

                diretorio[bucketAntigo] = '0' + diretorio[bucketAntigo]
                with open(diretorio[bucketNovo]+'.txt','w') as arq:
                    arq.write(f"{pl+1},0\n")

    for registro in registros:
        dados = registro.split(',')
        chave = int(dados[1][:-1])
        enderecoDiretorio = mascara(chave, pl+1)
        if(diretorio[enderecoDiretorio]==diretorio[bucketAntigo]):
            inserir(dados[0], chave,bucketAntigo, diretorio)
        else:
            inserir(dados[0], chave, bucketNovo, diretorio)

def removerBucket(indice_bucket,chave):
    with open(indice_bucket,'r') as bucket:
        tuplas = bucket.readlines()
    pl= tuplas[0].split(",")[0]
    
    for tupla in tuplas[1:]:
        if(tupla.split(",")[1][:-1] == str(chave)):
            tuplas.remove(tupla)

    with open(indice_bucket,"w") as bucket_alterado:
        tuplas[0] =f"{pl},{len(tuplas)-1}\n"
        
        for i in tuplas:
            bucket_alterado.write(i)
            
    return (pl,len(tuplas)-1)




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
        """print(f"{type(registrosBucketAmigo)}:{registrosBucketAmigo}")
        print(f"{type(registros_atuais)}:{registros_atuais}")"""
        if(registros_atuais[1]+registrosBucketAmigo<=32):
            #Se passa por este teste, então um bucket consegue comportar as entradas
            #Agora, deve-se verificar se todos os buckets da segunda metade do diretório tem profundidade
            #local menor que a global
            quantidade_teste = 0
            for i in range(tam_diretorio//2,tam_diretorio):
                
                if(len(diretorio[i]))>=pg:
                    quantidade_teste += 1
            if(quantidade_teste==1):
                #Significa que só há um bucket com pg==pl, logo o diretório pode ser reduzido
                FundirBucket(indice_bucket,indice_bucket_amigo,diretorio)

def FundirBucket(indice_bucket, indice_bucket_amigo, diretorio):
    if(indice_bucket<indice_bucket_amigo):
        indiceUsado = indice_bucket
        indiceRemovido = indice_bucket_amigo
    else:
        indiceUsado = indice_bucket_amigo
        indiceRemovido = indice_bucket
    
    with open(diretorio[indiceUsado]+'.txt','r') as arq1, open(diretorio[indiceRemovido]+'.txt','r') as arq2:
        pl_reg = arq1.readline().split(',')
        profundidadeLocal = int(pl_reg[0])
        quantRegistros1 = int(pl_reg[1][:-1])
        print(f"Quantidade de registros 1:{quantRegistros1}")
        registros1 = arq1.readlines()
        print(registros1)

        quantRegistros2 = int(arq2.readline().split(',')[1][:-1])
        print(f"Quantidade de registros 1:{quantRegistros2}")
        registros2 = arq2.readlines()

    with open(diretorio[indiceUsado]+'.txt', 'w') as arq:
        arq.write(f"{profundidadeLocal-1},{quantRegistros1+quantRegistros2}\n")

        for registro in registros1:
            arq.write(registro)
        
        for registro in registros2:
            arq.write(registro)

    shutil.move(diretorio[indiceUsado]+'.txt', diretorio[indiceUsado][1:]+'.txt')
    diretorio[indiceUsado] = diretorio[indiceUsado][1:]
    
    remove('./'+diretorio[indiceRemovido] +'.txt')
    
    tamDiretorio = len(diretorio)
    for registro in diretorio[tamDiretorio//2:]:
        diretorio.pop(i)


diretorio = ['00','01','10','11']
for nome in diretorio:
    with open(nome + '.txt', 'w') as arq:
        arq.write('2,0\n')

for i in range(33):
    inserir(80+i, 0+4*(i%2),0, diretorio)

for i in range(5):
    inserir(81,12,4,diretorio)
'''for i in range(33):
    inserir(80+i, 2+4*(i%2), 6, diretorio)
print(diretorio)'''

remover(diretorio,4)

print(diretorio)