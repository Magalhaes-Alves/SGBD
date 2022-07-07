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

    
    def undo_no_redo(self):
        #Função para fazer a etapa de análise,ou seja,inserir a transação na lista de Undo,Redo ou Rollback.
        self.analise()
        #Função para fazer a etapa de Undo, ou seja, desfazer as operações que sofreram rollack e depois as 
        #da Undo List
        self.undo()
        #Neste algoritmo não há a etapa de redo, mas é necessário refazer alterações da Undo List e da Rollback
        #list em conjunto.Esta função serve justamente a esse próposito.
        self.no_redo()

        #Printar as informações no terminal
        print("Undo/No-Redo")
        print(f"Undo list:{self.undo_list}")
        print(f"Rollback list:{self.rollback_list}")
        print("Estado recuperado")
        print(self.objetos)
    
    def analise(self):
        log_aux = self.log.log
        
        ativas = self.log.extrairTransacoes()
        #Pega todas as transações e coloca elas como ativas inicialmente.
        #Na iteração abaixo, vão sendo retiradas transações da lista conforme mostrado abaixo para
        # que as trasações restantes sejam colocadas na Undo List

        for i in range(len(log_aux)-1,-1,-1):
            #Percorre o log de trás pra frente para verificar em que lista a transação será colocada 
            if log_aux[i][3] == 'a':
                self.rollback_list.append(log_aux[i][2])
                #Coloca na lista de ativas
                ativas.remove(log_aux[i][2])
            
            if log_aux[i][3] == 'c':
                ativas.remove(log_aux[i][2])
                #Retira das transações ativas. 

        self.undo_list =ativas
        
        self.tabela_transacao = dict.fromkeys(ativas)
        
        
        for i in range(len(log_aux)-1,-1,-1):
            #Percorre novamente o log de trás pra frente para indicar em qual ponto do registro de log
            # está a última operação de uma transação ativa 
            if log_aux[i][2] in self.tabela_transacao.keys() and self.tabela_transacao[log_aux[i][2]] == None:
                self.tabela_transacao[log_aux[i][2]] = log_aux[i][0]
    
    def undo(self):
        #Primeiro, as operações que sofreram rollback serão desfeitas
        self.desfazer_alteracoes(self.rollback_list)

        #Após isso, serão desfeitas as operações da lista Undo
        self.desfazer_alteracoes(self.undo_list)

    def desfazer_alteracoes(self, trasacoes):
        
        if trasacoes ==[]:
            #Caso não haja transações para serem desfeitas, simplesmente retorna
            return
        
        log_aux = self.log.log

        for i in range(len(log_aux)-1,-1,-1):
            #Itera sobre o log de trás para frente.
            if log_aux[i][2] in trasacoes and log_aux[i][3]=='w':
                #Verifica se a transação da linha do log desta iteração é uma das transações passadas para
                #serem desfeitas e verifica se aquela linha do log é referente a uma operação de escrita,já que
                #nela houve alteração no valor.
                self.objetos[log_aux[i][4]] = log_aux[i][-2]
                #Na linha acima é lido o registro daquela linha para que o estado do item seja passado ao estado
                #ao estado anterior ao do comando de escrita.

    def no_redo(self):

        self.refazer_alteracoes(self.undo_list+self.rollback_list)

    def refazer_alteracoes(self, trasacoes):
        if trasacoes ==[]:
            #Se a lista de transações passada for vazia, simplesmente retorna.
            return
        
        log_aux = self.log.log

        for i in range(0,len(log_aux)-1):
            #Percorre o log,e, caso a transação não esteja na Undo List ou na Rollback list e 
            # a operação seja de escrita, as alterações relativas àquela operação são refeitas. 
            if (not log_aux[i][2] in trasacoes) and log_aux[i][3]=='w':
                self.objetos[log_aux[i][4]] = log_aux[i][-1]

