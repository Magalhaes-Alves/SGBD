from Log import Log

class Recuperacao:

    def __init__(self, nome_arquivo_log ):

        self._log = Log(nome_arquivo_log)

        self._undo =[]
        self._rollback =[]
        self._redo =[]
        self._tabela_trasacao =[]
        self._objetos = self._log.extraiObjetos()

        self.analise()
        self.undo_no_redo()

    
    def undo_no_redo(self):
        self.analise()

    
    def analise(self):
        aux = self.log.log
        
        ativas = self.log.extrairTransacoes()

        for i in range(len(aux)-1,-1,-1):
            
            if aux[i][3] == 'a':
                self.rollback.append(aux[i][2])
                ativas.remove(aux[i][2])
            
            if aux[i][3] == 'c':
               ativas.remove(aux[i][2]) 

        self.undo +=ativas
        self.tabela_trasacao = dict.fromkeys(ativas)

        for i in range(len(aux)-1,-1,-1):
            if aux[i][2] in self.tabela_trasacao.keys() and self.tabela_trasacao[aux[i][2]] == None:
                self.tabela_trasacao[aux[i][2]] = aux[i][0]
    
    def undo():
        pass

    @property
    def log(self):
        return self._log

    @property
    def rollback(self):
        return self._rollback
    
    @rollback.setter
    def rollback(self, novo):
        self._rollback = novo
    
    @property
    def undo(self):
        return self._undo
    
    @property
    def redo(self):
        return self._redo
    
    @undo.setter
    def undo(self, novo):
        self._undo = novo

    @property
    def tabela_trasacao(self):
        return self._tabela_trasacao

    @tabela_trasacao.setter
    def tabela_trasacao(self, novo):
        self._tabela_trasacao = novo
