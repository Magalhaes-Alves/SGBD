
""" 
Mascara de bits
Retorna os exatos b ultimos bits de um inteiro
""" 
import  shutil, tempfile
from math import log2

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
  
  with open(diretorio[bucket] + '.txt','r') as dados:
    pl_reg =dados.readline() 
    pl_reg= pl_reg.split(',') #[0] = pl ; [1] = qntd registro     

    if(int(pl_reg[1][:-1])<32):
        #Passo para adicionar em um a quantidade de registros no conteudo da linha
        quantidade_registros = pl_reg[1][:-1]
        quantidade_registros = int(quantidade_registros) +1
        pl_reg[1] = str(quantidade_registros)

        with tempfile.NamedTemporaryFile('w', delete=False) as out:
            out.write(f"{pl_reg[0]},{pl_reg[1]}\n")
            eof = False
        
            while(not (eof)):
                pl_reg = dados.readline()
                if pl_reg=='':
                    eof=True
                else:
                    out.write(pl_reg)
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


diretorio = ['00','01','10','11']
for nome in diretorio:
    with open(nome + '.txt', 'w') as arq:
        arq.write('2,0\n')

for i in range(30):
    inserir(80+i, 0+4*(i%2),0, diretorio)

'''for i in range(33):
    inserir(80+i, 2+4*(i%2), 6, diretorio)
print(diretorio)'''

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
    pg = int(log2(len(diretorio)))


    indice_bucket = mascara(chave_busca, pg)

    registros_atuais =removerBucket(diretorio[indice_bucket]+".txt",chave_busca)
    
    indice_balde_amigo = str(int(not(int(diretorio[indice_bucket][0]))))+diretorio[indice_bucket][1:]
    print(indice_balde_amigo)




remover(diretorio,0)