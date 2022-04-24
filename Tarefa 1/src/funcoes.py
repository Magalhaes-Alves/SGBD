
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
        shutil.move(out.name, bucket)

    else:
        pass    

def duplicarDiretorio(diretorio):

    tamanho_anterior= len(diretorio)
    for i in range(tamanho_anterior):
        diretorio.append('1'+diretorio[i])
        diretorio[i] = '0'+diretorio[i]


