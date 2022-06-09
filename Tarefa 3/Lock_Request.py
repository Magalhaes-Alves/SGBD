class Lock_Request():
    def __init__(self,modo, TR, prox, item):
        self._modo = modo
        self._TR = TR
        #Inteiro que referencia a transação, ou seja, a chave da transação em Tr_list
        self._prox = prox
        #Ponteiro para o proximo LockRequest para verificar se há ciclo
        self._item = item

    @property
    def TR(self):
        return self._TR

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
