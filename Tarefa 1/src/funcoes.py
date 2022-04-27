
""" 
Mascara de bits
Retorna os exatos b ultimos bits de um inteiro
""" 
import  shutil, tempfile

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
  
  with open(diretorio[bucket] + '.txt','r') as dados:
    pl_reg =dados.readline() 
    pl_reg= pl_reg.split(',') #[0] = pl ; [1] = qntd registro     
    
    if(int(pl_reg[1][:-1])<32):
        #Passo para adicionar em um a quantidade de registros no conteudo da linha
        quantidade_registros = list(pl_reg[1].strip())
        quantidade_registros[0] = str (int(quantidade_registros[0]) +1)
        pl_reg[1] = "".join(quantidade_registros)

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

    elif pl_reg[0]>=len(diretorio)/2:
        tam = len(diretorio)
        duplicarDiretorio(diretorio,bucket)
        divisaoBucket(bucket, bucket+ tam, diretorio)    
    else:
        divisaoBucket()

def duplicarDiretorio(diretorio,bucket):

    tamanho_anterior= len(diretorio)
    pl = len(diretorio[bucket])

    for i in range(tamanho_anterior):
        diretorio.append(diretorio[i])

    diretorio[bucket+tamanho_anterior] = '1' + diretorio[bucket]
    
    with open(diretorio[bucket]+'.txt','r') as arq:
        pl_reg =arq.readlines()
    
    with open(diretorio[bucket]+'.txt','w') as arq:
        arq.write(f"{pl+1},{pl_reg[0].split(',')[1]}")
        for registro in pl_reg[1:]:
            arq.write(registro)
    shutil.move(diretorio[bucket] + '.txt','0' + diretorio[bucket] + '.txt')
   
    diretorio[bucket] = '0' + diretorio[bucket] 
    
    #Criando o novo bucket para o bucket correspondente que disparou a duplicacao de diretorio
    with open(diretorio[bucket+tamanho_anterior]+'.txt','w') as bucketNovo:
        bucketNovo.write(f"{pl+1},0\n")
    print(diretorio)


def divisaoBucket(bucketAntigo,bucketNovo,diretorio):
    pl = len(diretorio[bucketAntigo])
    
    
    #Isto é o equivalente a carregar o bucket para a memória principal para que se possa fazer a divisao
    with open(diretorio[bucketAntigo] + '.txt','r') as arq:
        registros = arq.readlines()[1:]
    
    with open(diretorio[bucketAntigo] + '.txt','w') as arq:
        arq.write(f"{pl},0\n")

    with open(diretorio[bucketNovo] + '.txt','w') as arq:
        arq.write(f"{pl},0\n")

    for registro in registros:
        dados = registro.split(',')
        chave = int(dados[1][:-1])
        enderecoDiretorio = mascara(chave, pl)
        if(enderecoDiretorio==bucketAntigo):
            inserir(dados[0], chave,bucketAntigo, diretorio)
        else:
            inserir(dados[0], chave, bucketNovo, diretorio)

diretorio = ['00','01','10','11']

duplicarDiretorio(diretorio,0)
#divisaoBucket(0,2,diretorio)

def removerBucket(indice_bucket,chave):
    with open(indice_bucket,'r') as bucket:
        tuplas = bucket.readlines()
    pl= tuplas[0].split(",")[0]
    
    for i in range(1,len(tuplas)):
        if(tuplas[i].split()[1] ==str(chave)):
            tuplas.pop(i)
    with open(indice_bucket,"w") as bucket_alterado:
        tuplas[0] =f"{pl},{len(tuplas)-1}"
        for i in tuplas:
            bucket_alterado.write(i)
    return len(tuplas)




def remover(diretorio,chave_busca,pg):

    indice_bucket = enderecoBucket(chave_busca, pg)

    removerBucket(diretorio[indice_bucket]+".txt",chave)


    pass