from Transacao import Transacao

class Tr_Manager():
    def __init__(self):
        self._Tr_List = {}
        self._TR_Atual = 0
        """
        Número associado ao Tr que tem no enunciado.Não entendi muito bem o que queria dizer, então fiz um dicionário
        em que a chave é este valor de Tr e o valor é a transação em si com os atributos.Assim, o self.TR_List[Tr].Id
        pode ser entendido como o Tr.Id descrito no enunciado
        """
        self._TS_Atual = 0
        self._waitForDataList= {}
        """
        Guarda os itens em que há operações em espera relativas a determinada transação.
        Isto é guardado é um dicionário de tal forma que TR é a chave e o valor relativo a essa chave é uma
        lista em que o primeiro elemento é um inteiro que sinaliza o seguinte de acordo com seu valor:
        -1 : Transação Postergada
        0 : Transação ativa com operações em espera
        1: Transação ativa sem operações em espera

        O resto dos elementos da lista são os itens em que há operações daquela transação em espera
        """
        self._grafo = []
    
    @property
    def grafo(self):
        return self._grafo

    @property
    def TS_Atual(self):
        return self._TS_Atual
    
    @property
    def TR_Atual(self):
        return self._TR_Atual

    @property
    def Tr_List(self):
        return self._Tr_List

    @property
    def waitForDataList(self):
        return self._waitForDataList
    
    @waitForDataList.setter
    def waitForDataList(self, novo):
        self._waitForDataList = novo

    def aumentar_TS(self):
        self._TS_Atual +=1

    def aumentar_TR(self):
        self._TR_Atual +=1

    def get_TR(self,TR):
        return self.Tr_List[TR]
    
    def inserir(self,TR_Novo):
        (self.Tr_List)[self.TR_Atual] = TR_Novo
        self.waitForDataList[self.TR_Atual] = [1]
        #O primeiro elemento é o 1 para indicar que é uma transação ativa sem operações em espera
        self.aumentar_TR()
    
    def remover(self,TR):
        self.Tr_List.pop(TR, "NExiste")

    def atualizar_status(self, TR, Novo_Status):
        self.Tr_List[TR].status = Novo_Status

    def buscar_TR_por_Id(self, Id):
        chaves = self.Tr_List.keys()

        for chave in chaves:
            if(self.Tr_List[chave].Id == Id):
                return chave
        
        #Para indicar que não foi encontrada Transação com este Id
        return -1
    

    def Printar_Tr_Manager(self):
        chaves = self.Tr_List.keys()

        for chave in chaves:
            TR = self.Tr_List[chave]
            print(f"TR:{chave}")
            print(f"Id:{TR.Id}, TS:{TR.Ts}, Status:{TR.status}\n")