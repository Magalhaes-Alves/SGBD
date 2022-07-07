
#Essa classe irá armazenar totas as historias 

class Log:

    def __init__(self,arquivo):
        self._log= []
        with open(arquivo, 'r') as historias:
            self._log = historias.readlines()
            self._log = list(map(lambda x: x[2:-3].split(' | '),self._log))

    def mostrarLog(self):
        for i in range(len(self._log)):
            print(f'[{self._log[i]}]\n')

    @property
    def log(self):
        return self._log


    def extrairTransacoes(self):
        #Função para extrair as transações do Log percorrendo todo ele
        transacoes =[]
        for i in self._log:
            if not i[2] in transacoes:
                transacoes.append(i[2])
        return transacoes

    def extraiObjetos (self):
        objetos={}
        for i in self._log:
            #Percorre o log e atribui a label do objeto ao dicionário de objetos 
            if i[3] in 'wr':
                objetos.setdefault(i[4],None)
        return objetos
