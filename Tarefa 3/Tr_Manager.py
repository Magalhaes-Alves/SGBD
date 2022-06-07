from Transacao import Transacao

class Tr_Manager():
    def __init__(self):
        self.Tr_List = {}
        self._TS_Atual = 0

    
    def get_TR(self,TR_Id):
        return self.Tr_List[TR_Id]

    
    def inserir(self,TR_Novo):
        self.Tr_List[TR_Novo.Id] = TR_Novo

    
    def remover(self,TR_Id):
        self.Tr_List.pop(TR_Id, "NExiste")
    
    def atualizar_status(self, TR_Id, Novo_Status):
        self.Tr_List[TR_Id].status = Novo_Status

    