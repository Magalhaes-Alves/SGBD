class Lock_Request():
    def __init__(self, modo, TR_Id, prox, item):
        self._modo = modo
        self._TR_Id = TR_Id
        #String que referencia o id da transação.Como há uma função para buscar TR pelo ID,
        #pode-se encontrar a chave da transação em Tr_list a partir do atributo TR_Id
        self._prox = prox
        #Ponteiro para o proximo LockRequest da lista Lock_Table ou WaitQ
        self._item = item


    @property
    def TR_Id(self):
        return self._TR_Id

    @property
    def modo(self):
        return self._modo

    @property
    def prox(self):
        return self._prox

    @prox.setter
    def prox(self, Novo_Prox):
        self._prox = Novo_Prox

    @property
    def item(self):
        return self._item
