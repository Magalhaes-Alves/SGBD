class Lock_Request():
    def __init__(self, pageid, modo, tr, prox):
        self._pageid = pageid
        self.modo = modo
        #Inteiro que referencia a transação, ou seja, a posição da transação em Tr_list
        self._tr = tr
        #Ponteiro para o proximo LockRequest
        self.prox = prox
