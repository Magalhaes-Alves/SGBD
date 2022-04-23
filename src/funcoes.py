
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
    
    with open(bucket,'r') as dados:
        dados.readline()
        flag =False
        eof = False
        while(not(flag or eof)):
            linha = dados.readline()
            if linha=='':
                eof=True
            else:
                if int(linha.split(',')[2])== chave_busca:
                    flag =True
        return (flag,linha)

def busca(chave, diretorio):
    pass


