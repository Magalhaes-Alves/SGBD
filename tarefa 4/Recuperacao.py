from Log import Log

class Recuperacao:

    def __init__(self, nome_arquivo_log ):

        self._log = Log(nome_arquivo_log)

        self._undo_list =[]
        self._rollback_list =[]
        self._redo_list =[]
        self._tabela_transacao ={}
        self._objetos = self._log.extraiObjetos()

        self.undo_no_redo()

    
    def undo_no_redo(self):
        self.analise()
        self.undo()
        self.no_redo()
        print(self.objetos)
    
    def analise(self):
        log_aux = self.log.log
        
        ativas = self.log.extrairTransacoes()

        for i in range(len(log_aux)-1,-1,-1):
            
            if log_aux[i][3] == 'a':
                self.rollback_list.append(log_aux[i][2])
                ativas.remove(log_aux[i][2])
            
            if log_aux[i][3] == 'c':
                ativas.remove(log_aux[i][2]) 

        self.undo_list =ativas
        
        self.tabela_transacao = dict.fromkeys(ativas)
        
        
        for i in range(len(log_aux)-1,-1,-1):
            if log_aux[i][2] in self.tabela_transacao.keys() and self.tabela_transacao[log_aux[i][2]] == None:
                self.tabela_transacao[log_aux[i][2]] = log_aux[i][0]
    
    def undo(self):
        #primeiro irei desfazer as operações que sofreram rollback
        #print(self.objetos)
        self.desfazer_alteracoes(self.rollback_list)
        #print(self.objetos)

        self.desfazer_alteracoes(self.undo_list)

    def desfazer_alteracoes(self, trasacoes):
        
        if trasacoes ==[]:
            return
        
        log_aux = self.log.log

        for i in range(len(log_aux)-1,-1,-1):
            if log_aux[i][2] in trasacoes and log_aux[i][3]=='w':
                self.objetos[log_aux[i][4]] = log_aux[i][-2]

    def no_redo(self):

        self.refazer_alteracoes(self.undo_list+self.rollback_list)

    def refazer_alteracoes(self, trasacoes):
        if trasacoes ==[]:
            return
        
        log_aux = self.log.log

        for i in range(0,len(log_aux)-1):
            if (not log_aux[i][2] in trasacoes) and log_aux[i][3]=='w':
                self.objetos[log_aux[i][4]] = log_aux[i][-1]




    @property
    def log(self):
        return self._log

    @property
    def rollback_list(self):
        return self._rollback_list
    
    @property
    def undo_list(self):
        return self._undo_list
    
    @undo_list.setter
    def undo_list(self, novo):
        self._undo_list = novo

    @property
    def redo_list(self):
        return self._redo_list
    
    @property
    def tabela_transacao(self):
        return self._tabela_transacao

    @tabela_transacao.setter
    def tabela_transacao(self,novo):
        self._tabela_transacao = novo

    @property
    def objetos(self):
        return self._objetos

    @property
    def commit(self):
        return self._commit

    