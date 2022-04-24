
""" 
Mascara de bits
Retorna os exatos b ultimos bits de um inteiro
""" 
import readline


def mascara(inteiro, b):
    mask = 2**(b)-1
    return inteiro & mask

def funcaoHashing(chave_busca):
    return bin(chave_busca)

def buscarBucket(chave_busca,bucket):
    dados_bucket = []
    with open(bucket,'r') as dados:
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
  
def inserir(id_vinho,chave_busca,bucket):
  with open(bucket,'r') as dados:
    pl_reg =dados.readline() 
    pl_reg= pl_reg.split(',') #[0] = pl ; [1] = qntd registro     
    print(pl_reg)
    if(int(pl_reg[1][:-1])<32):
      with open(bucket, 'a') as arq:
        arq.write(f"{id_vinho},{chave_busca}\n")
    else:
      pass    


