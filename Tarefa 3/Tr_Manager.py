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

    
    @property
    def TS_Atual(self):
        return self._TS_Atual
    
    @property
    def TR_Atual(self):
        return self._TR_Atual

    @property
    def Tr_List(self):
        return self._Tr_List

    def aumentar_TS(self):
        self._TS_Atual +=1

    def aumentar_TR(self):
        self._TR_Atual +=1

    def get_TR(self,TR_Id):
        return self.Tr_List[str(TR_Id)]
    
    def inserir(self,TR_Novo):
        (self.Tr_List)[self.TR_Atual] = TR_Novo
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