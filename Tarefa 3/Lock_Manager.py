from Tr_Manager import Tr_Manager
from Transacao import Transacao
from Lock_Request import Lock_Request


class Lock_Manager():
    def __init__(self, OPS, tipo_Prevencao):
        self._Lock_Table = {}
        """
        Neste dicionário, a chave é o item e o valor relativo a uma chave é a lista de Lock_Requests associados àquele item.
        Esta lista é percorrida a partir do ponteiro para próximo.
        """

        with open('Lock_Table.txt', 'w') as arq:
            arq.write("Item,Lock,Tr_Id\n")

        self._WaitQ = {}
        self._CommitsEmEspera = []
        self.tr_manager = Tr_Manager()
        self._OPS = OPS
        self._OPS_Postergadas = {}
        self._tipo_Prevencao = tipo_Prevencao

    @property
    def tipo_Prevencao(self):
        return self._tipo_Prevencao

    @property
    def OPS(self):
        return self._OPS

    @property
    def OPS_Postergadas(self):
        return self._OPS_Postergadas

    @property
    def CommitsEmEspera(self):
        return self._CommitsEmEspera

    @property
    def WaitQ(self):
        return self._WaitQ

    @WaitQ.setter
    def WaitQ(self, novo):
        self._WaitQ = novo

    @property
    def Lock_Table(self):
        return self._Lock_Table

    @Lock_Table.setter
    def Lock_Table(self,novo):
        self._Lock_Table = novo


    def Carregar_Lock_Table(self):
        arq = open('Lock_Table.txt', 'r')
        registros = arq.readlines()
        arq.close()
        
        for registro in registros[1:]:
            atributos = registro.split(',')
            #TR = self.tr_manager.buscar_TR_por_Id(atributos[2])
            
            Novo_Lock_Request = Lock_Request(atributos[1], atributos[2][:-1], None, atributos[0])

            chaves = self.Lock_Table.keys()
            if atributos[0] in chaves:
                "Coloca no final da Lista associada a esse item"
                aux = self.Lock_Table[atributos[0]]
                while(aux.prox != None):
                    aux = aux.prox
                aux.prox = Novo_Lock_Request
            else:
                "Cria a lista associada a esse item"
                self.Lock_Table[atributos[0]] = Novo_Lock_Request
        

    def Printar_Lock_Table(self):
        print("--LockTable--")
        chaves = self.Lock_Table.keys()
        for chave in chaves:
            aux = self.Lock_Table[chave]
            while(aux != None):
                print(f"Item:{aux.item},Lock:{aux.modo},Tr_Id:{aux.TR_Id}\n")
                aux = aux.prox


    def Escrever_Lock_Table(self):
        chaves = self.Lock_Table.keys()
        arq = open('Lock_Table.txt', 'w')
        arq.write("Item,Lock,Tr_Id\n")
        
        for chave in chaves:
            aux = self.Lock_Table[chave]
            #Id_TR = self.tr_manager.get_TR(aux.TR).Id
            while(aux != None):
                arq.write(f'{aux.item},{aux.modo},{aux.TR_Id}\n')
                aux = aux.prox
        
        arq.close()
        self.Lock_Table = {}


    def printar_WaitQ(self):
        print("--WAITQ--")
        chaves = self.WaitQ.keys()
        for chave in chaves:
            aux = self.WaitQ[chave]
            while(aux != None):
                print(f"Item:{aux.item},Lock:{aux.modo},Tr_Id:{aux.TR_Id}\n")
                aux = aux.prox


    def postergarTR(self,Lock_Request_Aux, transacoes):
        TR_ID = Lock_Request_Aux.TR_Id
        modo = 'r' if Lock_Request_Aux.modo == 'S' else 'w'
        item = Lock_Request_Aux.item

        #Cria as listas de operações postergadas para cada um
        
        print(transacoes)
        for transacao in transacoes:
            self.OPS_Postergadas[transacao] = []
  
        i = 0
        
        while(self.OPS[i].tipo[0] != modo or self.OPS[i].tipo[1] != TR_ID or self.OPS[i].item !=item):
            #Iterar sobre a lista de operações até a operação atual
            if((self.OPS[i].tipo[0] ==  'r' or self.OPS[i].tipo[0] ==  'w') and self.OPS[i].tipo[1] in transacoes):
                
                self.OPS_Postergadas[self.OPS[i].tipo[1]].append((self.OPS[i]))
                #Se a operação de uma dada iteração for relativa à mesma transação da que está sendo postergada,
                # a operação é retirada da lista em que estiver(Lock_Table ou WaitQ) e colocada na lista de 
                # operações Postergadas
                chaves = self.Lock_Table.keys()
                verificaWait = True 
                #Procurar na lockTable pelo item.Se não estiver na LockTale procurar na lista de espera
                if item in chaves:
                    Corrente = self.Lock_Table[self.OPS[i].item]
            
                    Anterior = None
                    while (Corrente != None and verificaWait==True):
                        Seguinte = Corrente.prox
                        if self.OPS[i].tipo[1] == Corrente.TR_Id:                
                            if Anterior == None:
                                self.Lock_Table[self.OPS[i].item] = Corrente.prox
                                Corrente = None
                            elif Seguinte == None:
                                Anterior.prox = None
                            else:
                                Anterior.prox = Corrente.prox
                            verificaWait = False
                        Anterior = Corrente
                        Corrente = Seguinte

                    if(self.Lock_Table[self.OPS[i].item]==None):
                        self.Lock_Table.pop(self.OPS[i].item)
                
                #Procurar na WaitQ
                if verificaWait==True:
                    Corrente = self.WaitQ[self.OPS[i].item]

                    Anterior = None
                    while (Corrente != None):
                        Seguinte = Corrente.prox
                        if self.OPS[i].tipo[1] == Corrente.TR_Id:                
                            if Anterior == None:
                                self.WaitQ[self.OPS[i].item] = Corrente.prox
                                Corrente = None
                            elif Seguinte == None:
                                Anterior.prox = None
                            else:
                                Anterior.prox = Corrente.prox
                            break
                        Anterior = Corrente
                        Corrente = Seguinte

                    if(self.WaitQ[self.OPS[i].item]==None):
                        self.WaitQ.pop(self.OPS[i].item)
            
            i+=1
        
        
        for transacao in transacoes:
            self.tr_manager.waitForDataList[transacao] = [-1]
        if TR_ID not in transacoes:
            return True
        else:
            self.OPS_Postergadas[self.OPS[i].tipo[1]].append(self.OPS[i])

    def rollBack(self, transacoes,Lock_Request_Postergado):
        #Deve-se colocar as operações relativas a trans_Adicionada na fila de transações postergadas
        if(self.postergarTR(Lock_Request_Postergado, transacoes)):
            chaves = self.Lock_Table.keys()
            if Lock_Request_Postergado.item in chaves:
                aux_Lock  = self.Lock_Table[Lock_Request_Postergado.item]
                while(aux_Lock.prox!=None):
                    aux_Lock = aux_Lock.prox
                aux_Lock.prox = Lock_Request_Postergado
            else:
                self.Lock_Table[Lock_Request_Postergado.item] = Lock_Request_Postergado
       

        
        itensLiberados = []
        for transacao in transacoes:
            for operacao in self.OPS_Postergadas[transacao]:
                itensLiberados.append(operacao.item)
            
        #Deve-se tentar executar operações de transações ativas em espera.Caso alguma transação seja commitada
        #neste proccesso, deve-se tentar executar novamente operações de transações ativas em espera.
        
        self.liberar_itens_WaitQ(itensLiberados,transacoes)
        
        self.commitar(-1,True)
        #Finalmente, deve-se tentar reiniciar as transações de acordo com sua ordem na fila de transações postergadas
        self.Reiniciando()
        
       
    def Reiniciando(self):
        print("Reiniciando Transações Postergadas...")
        tentativas = len(self.OPS_Postergadas)
        while(tentativas>0):
            tentativas -= 1
            self.Escrever_Lock_Table()
            TR_Topo = list(self.OPS_Postergadas.keys())[0]
            TR_Topo = (sorted(self.OPS_Postergadas, key = lambda p:self.tr_manager.get_TR(self.tr_manager.buscar_TR_por_Id(p)).Ts))[0]
            TR_aux = self.tr_manager.buscar_TR_por_Id(TR_Topo)
            for operacao in self.OPS_Postergadas[TR_Topo]:
                if operacao.tipo[0] == 'r':
                    print(f'r{TR_Topo}({operacao.item})-', end = '')
                    self.LS(TR_aux,operacao.item)
                else:
                    print(f'w{TR_Topo}-({operacao.item})', end = '')
                    self.LX(TR_aux,operacao.item)
            
            aux_Commitar = False
            if TR_Topo in self.CommitsEmEspera:
                aux_Commitar = True
            if aux_Commitar == True:
                self.OPS_Postergadas.pop(TR_Topo)
                self.commitar(TR_Topo)
            
            self.Carregar_Lock_Table()

    def waitDie(self,TR, item, Novo_Lock_Request):

        trans_Adicionada = self.tr_manager.get_TR(TR)
        #Transação que ocasionou a execução do wait-die
        trans_Enfileirada = self.tr_manager.buscar_TR_por_Id(Novo_Lock_Request.TR_Id)
        #Pega o TR e na linha seguinte pega a transação em si
        if trans_Enfileirada!=-1:
            trans_Enfileirada = self.tr_manager.get_TR(trans_Enfileirada)
        #Verifica se a transação está em espera
        if self.tr_manager.waitForDataList[TR][0] == 0:
            aux_Lock = None
        else:
            aux_Lock = self.Lock_Table[item]
            
        count = 0
        
        while(aux_Lock != None):
            aux_Trans = self.tr_manager.buscar_TR_por_Id(aux_Lock.TR_Id)
            #Pega o TR e na linha seguinte pega a transação em si
            aux_Trans = self.tr_manager.get_TR(aux_Trans)
            

            if trans_Adicionada.Ts > aux_Trans.Ts and aux_Lock.modo == 'X':
                #A transação de trans_Adicionada deve ser postergada devido a uma situação de ROLLBACK
                print(f"RollBack TS({trans_Adicionada.Id})>TS({aux_Trans.Id})")
                #print(f"Novo:{Novo_Lock_Request.item}")
                #print(f"Chaves:{self.WaitQ.keys()}")
                if Novo_Lock_Request.item in self.WaitQ.keys():
                    listaparam = self.WaitQ[Novo_Lock_Request.item]
                else:
                    listaparam = Novo_Lock_Request.item
                self.tr_manager.printarGrafo(listaparam)
                self.rollBack([trans_Adicionada.Id], Novo_Lock_Request)
                self.tr_manager.printarGrafo()
                return

            count += 1
            aux_Lock = aux_Lock.prox
            
        
        #Coloca na Lista de Espera
        print("Em espera")
        self.tr_manager.waitForDataList[TR][0] = 0
        self.tr_manager.waitForDataList[TR].append(item)
        #Muda este valor para informar que há operações em espera
        if item in self.WaitQ.keys():
            
            #Coloca no final da lista de espera associada a este item
            aux_Lock = self.WaitQ[item]
            while aux_Lock.prox != None:
                aux_Lock = aux_Lock.prox

            aux_Lock.prox = Novo_Lock_Request
        else:
            
            self.WaitQ[item] = Novo_Lock_Request
        
        #Adiciona as arestas ao grafo
        if Novo_Lock_Request.item in self.Lock_Table.keys():
            aux_Lock = self.Lock_Table[Novo_Lock_Request.item]
            while(aux_Lock!=None):
                if Novo_Lock_Request.TR_Id!=aux_Lock.TR_Id:
                    self.tr_manager.AdicionarArestaGrafo(Novo_Lock_Request.TR_Id, aux_Lock.TR_Id)
                aux_Lock = aux_Lock.prox
    

    def woundWait(self,TR, item, Novo_Lock_Request):
        self.Printar_Lock_Table()
        trans_Adicionada = self.tr_manager.get_TR(TR)
        #Transação que ocasionou a execução do wait-die
        transRollBack = []
        
        trans_Enfileirada = self.tr_manager.buscar_TR_por_Id(Novo_Lock_Request.TR_Id)
        #Pega o TR e na linha seguinte pega a transação em si
        if trans_Enfileirada!=-1:
            trans_Enfileirada = self.tr_manager.get_TR(trans_Enfileirada)
        #Verifica se a transação está em espera
        if self.tr_manager.waitForDataList[TR][0] == 0:
            aux_Lock = None
        else:
            aux_Lock = self.Lock_Table[item]
            
        count = 0
        
        while(aux_Lock != None):
            
            aux_Trans = self.tr_manager.buscar_TR_por_Id(aux_Lock.TR_Id)
            #Pega o TR e na linha seguinte pega a transação em si
            aux_Trans = self.tr_manager.get_TR(aux_Trans)
            
            if trans_Adicionada.Ts < aux_Trans.Ts and Novo_Lock_Request.modo =='X':
                #A transação de trans_Adicionada deve ser postergada devido a uma situação de ROLLBACK
                count+=1
                transRollBack.append(aux_Trans.Id)
                
            aux_Lock = aux_Lock.prox
       
        self.Printar_Lock_Table()
        if count>0:
            transRollBack = list(set(transRollBack))
            for transacao in transRollBack:
                print(f"RollBack TS({trans_Adicionada.Id})<TS({transacao})")
            
            if Novo_Lock_Request.item in self.WaitQ.keys():
                listaparam = self.WaitQ[Novo_Lock_Request.item]
            else:
                listaparam = Novo_Lock_Request.item
            self.tr_manager.printarGrafo(listaparam)
            self.rollBack(transRollBack, Novo_Lock_Request)
            self.tr_manager.printarGrafo()
            return

        #Coloca na Lista de Espera
        print("Em espera")
        self.tr_manager.waitForDataList[TR][0] = 0
        self.tr_manager.waitForDataList[TR].append(item)
        #Muda este valor para informar que há operações em espera
        if item in self.WaitQ.keys():
            
            #Coloca no final da lista de espera associada a este item
            aux_Lock = self.WaitQ[item]
            while aux_Lock.prox != None:
                aux_Lock = aux_Lock.prox

            aux_Lock.prox = Novo_Lock_Request
        else:
            
            self.WaitQ[item] = Novo_Lock_Request
        
        #Adiciona as arestas ao grafo
        if Novo_Lock_Request.item in self.Lock_Table.keys():
            aux_Lock = self.Lock_Table[Novo_Lock_Request.item]
            while(aux_Lock!=None):
                if Novo_Lock_Request.TR_Id!=aux_Lock.TR_Id:
                    self.tr_manager.AdicionarArestaGrafo(Novo_Lock_Request.TR_Id, aux_Lock.TR_Id)
                aux_Lock = aux_Lock.prox


    def adicionarOPSPostergadas(self,TR_Id, modo, item):
        #Vai até a Operation na lista de Operations e adiciona o endereço dela ao final da respectiva lista de
        #Operações postergadas daquela transação
        i = 0
        while(self.OPS[i].tipo[0] != modo or self.OPS[i].tipo[1] != TR_Id or self.OPS[i].item !=item):
            i+=1
        self.OPS_Postergadas[TR_Id].append(self.OPS[i])


    def LS(self, TR, item):
        #insere um bloqueio no modo compartilhado na Lock_Table se puder,
		#senao insere um Lock_Request da transacao Tr na Wait_Q de D
        self.Carregar_Lock_Table()

        chaves = self.Lock_Table.keys()
        trans =(self.tr_manager.get_TR(TR))
        Novo_Lock_Request = Lock_Request("S", trans.Id,None, item)
        
        #Será que a transação em questão está com uma operação anterior em espera?
        if self.tr_manager.waitForDataList[TR][0] == 0:
            if self.tipo_Prevencao == 1:
                self.waitDie(TR, item, Novo_Lock_Request)
            else:
                self.woundWait(TR, item, Novo_Lock_Request)
        elif self.tr_manager.waitForDataList[TR][0] == -1:
            self.adicionarOPSPostergadas(trans.Id, 'r', item)
        elif (not item in chaves):
            #Significa que não há Pedido de bloqueio para este item
            self.Lock_Table[item] = Novo_Lock_Request
            print("OK")
        elif self.Lock_Table[item].modo == 'S':
            """Se todos os bloqueios forem do tipo compartilhado, adiciona operação no final"""
            aux_Lock = self.Lock_Table[item]
            aux_Cond = False
            while(aux_Lock.prox!=None and aux_Cond==False):
                if(aux_Lock.prox.modo=='X'):
                    aux_Cond = True
                aux_Lock = aux_Lock.prox
            if aux_Cond ==False:
                aux_Lock.prox = Novo_Lock_Request
                print("OK")
            else:
                if self.tipo_Prevencao == 1:
                    self.waitDie(TR, item, Novo_Lock_Request)
                else:
                    self.woundWait(TR, item, Novo_Lock_Request)
        else:
            #Situação em que self.Lock_Table[item].modo == 'D'
            if self.tipo_Prevencao == 1:
                self.waitDie(TR, item, Novo_Lock_Request)
            else:
                self.woundWait(TR, item, Novo_Lock_Request)

        self.Escrever_Lock_Table()


    def LX(self, TR, item):
        #Insere um bloqueio no modo exclusivo na Lock_Table
        self.Carregar_Lock_Table()

        trans = self.tr_manager.get_TR(TR)
        chaves = self.Lock_Table.keys()
        Novo_Lock_Request = Lock_Request("X", trans.Id,None, item)

        #Será que a transação em questão está com uma operação anterior em espera?
        if self.tr_manager.waitForDataList[TR][0] == 0:
            if self.tipo_Prevencao == 1:
                self.waitDie(TR, item, Novo_Lock_Request)
            else:
                self.woundWait(TR, item, Novo_Lock_Request)
        elif  self.tr_manager.waitForDataList[TR][0] == -1:
            self.adicionarOPSPostergadas(trans.Id, 'w', item)
        elif (not item in chaves):
            #Significa que não há Pedido de bloqueio para este item
            self.Lock_Table[item] = Novo_Lock_Request
            print("OK")
        elif self.Lock_Table[item].modo =='S' and self.tr_manager.buscar_TR_por_Id(self.Lock_Table[item].TR_Id)==TR:
            aux_Lock = self.Lock_Table[item]
            aux_Cond = False
            while(aux_Lock.prox!=None and aux_Cond==False):
                if(aux_Lock.prox.modo=='X' or self.tr_manager.buscar_TR_por_Id(aux_Lock.prox.TR_Id)!=TR):
                    aux_Cond = True
                aux_Lock = aux_Lock.prox
            if aux_Cond ==False:
                aux_Lock.prox = Novo_Lock_Request
                print("OK")
            else:
                if self.tipo_Prevencao == 1:
                    self.waitDie(TR, item, Novo_Lock_Request)
                else:
                    self.woundWait(TR, item, Novo_Lock_Request)
        else:
            #Senão , a página está bloqueada
            #Prevenção de Deadlock
            if self.tipo_Prevencao == 1:
                self.waitDie(TR, item, Novo_Lock_Request)
            else:
                self.woundWait(TR, item, Novo_Lock_Request)
        
        self.Escrever_Lock_Table()


    def U(self, TR, item,apagar):
        """Apaga os bloqueios da transacao Tr em relação a determinado item da Lock_Table"""

        trans = self.tr_manager.get_TR(TR)
        
        Corrente = self.Lock_Table[item]
        saida = False

        Anterior = None
        while (Corrente != None):
            
            Seguinte = Corrente.prox
            if trans.Id == Corrente.TR_Id:               
                if Anterior == None:
                    self.Lock_Table[item] = Corrente.prox
                    Corrente = None
                elif Seguinte == None:
                    Anterior.prox = None
                else:
                    Anterior.prox = Corrente.prox
                saida = True
            Anterior = Corrente
            Corrente = Seguinte
        
        if(self.Lock_Table[item]==None):
            apagar.append(item)

        
        return saida


    def ajustar_WaitforData(self):
        #Função para passar por todas as Listas de esperas das transações após a liberação de itens da WaitQ
        #para verificar se os itens na WaitForDataLista são de operações que estão na LockTable e apenas estavam em espera
        chaves = self.tr_manager.waitForDataList.keys()
        chaves2 = self.WaitQ.keys()
        itensLiberados = []
        transacoes = []
        for chave in chaves:
            listaTR = self.tr_manager.waitForDataList[chave]

            if(len(listaTR)==1):
                #Se todos os bloqueios em espera daquela transação puderam ir para a LockTable
                self.tr_manager.waitForDataList[chave] = [1]
            else:
                #Vai iterar novamente pela ListaTR para ver se há itens que podem ser liberados
                chavesLocks = self.Lock_Table.keys()
                for item in listaTR[1:]:
                    if item in chavesLocks:
                        #Verifica se há como mover o bloqueio para a LockTable
                        auxLock = self.Lock_Table[item]
                        aux2 = True
                        while(auxLock!=None and aux2==True):
                            if(auxLock.modo == 'X'):
                                aux2=False
                            auxLock = auxLock.prox
                        if(auxLock==None and aux2==True):
                            itensLiberados.append(item)
                            transacoes.append(self.tr_manager.get_TR(int(chave)).Id)
                    else:
                        itensLiberados.append(item)
                        transacoes.append(self.tr_manager.get_TR(int(chave)).Id)
       
        return (itensLiberados, transacoes)         


    def liberar_itens_WaitQ(self, itens_Liberados,transacoesArestas):
        aux = True
        transacoes = []
        while(aux==True):
            aux = False
            apagar = []
            for item_liberado in itens_Liberados:
            #Verifica se a WaitQ tem Transacoes associadas ao item que foi liberado
                chaves2 = self.WaitQ.keys()
                if item_liberado in chaves2:
                    #Se há transações associadas a esse item na lista de Espera.O primeiro bloqueio
                    #da lista de espera é pego
                    Corrente = self.WaitQ[item_liberado]
                    TR_Id_Aux = Corrente.TR_Id
                    #É pego o TR_Id do primeiro item para pegar todos os bloqueios da WaitQ com este bloqueio
                    Anterior = None
                    while (Corrente != None):
                        Seguinte = Corrente.prox
                        if TR_Id_Aux == Corrente.TR_Id:
                            #print(f"TR_ID:{TR_Id_Aux},Corrente.TR_Id:{Corrente.TR_Id}")
                            aux_Excluir = Corrente
                        
                            for transacao in transacoesArestas:
                                self.tr_manager.eliminarArestaGrafo(transacao)
                            #Apagar o Bloqueio em questão da WaitQ   
                            if Anterior == None:
                                self.WaitQ[item_liberado] = Corrente.prox
                                Corrente = None
                            elif Seguinte == None:
                                Anterior.prox = None
                            else:
                                Anterior.prox = Corrente.prox
                            #Mover bloqueio excluido para a LockTable
                            aux_Excluir.prox = None
                            chaves = self.Lock_Table.keys()
                            if item_liberado not in chaves:
                                self.Lock_Table[item_liberado] = aux_Excluir
                            else:
                                LockTable_aux = self.Lock_Table[item_liberado]
                                while(LockTable_aux.prox!=None):
                                    LockTable_aux = LockTable_aux.prox
                                LockTable_aux.prox = aux_Excluir

                            #Excluir itens liberados da WaitForDataList
                            TR = self.tr_manager.buscar_TR_por_Id(TR_Id_Aux)
                            self.tr_manager.waitForDataList[TR].remove(item_liberado)
                            #Mostrar a tentativa de execução
                            modo = 'r' if aux_Excluir.modo == 'S' else 'w'
                            print(modo + f"{TR_Id_Aux}({aux_Excluir.item}) - OK")
                            self.tr_manager.printarGrafo()

                        Anterior = Corrente
                        Corrente = Seguinte

                    
                    if(self.WaitQ[item_liberado]==None):
                        apagar.append(item_liberado)
            
            for apagaritem in apagar:
                self.WaitQ.pop(apagaritem)
            
            itens_Liberados, transacoes = self.ajustar_WaitforData()
            
            if len(itens_Liberados)>0:
                aux = True

    def commitar(self,commitExcluido, Aux=False):
        #Variável para entrar no loop a seguir e saber se alguma Transação foi commitada
        if int(commitExcluido)<0:
            TR_Aux = -1
        else:
            TR_Aux = self.tr_manager.buscar_TR_por_Id(commitExcluido)
            if self.tr_manager.waitForDataList[TR_Aux][0] == 1:       
                chaves = self.Lock_Table.keys()
                itens_Liberados = []
                apagar = []
                for chave in chaves:
                    if(self.U(TR_Aux, chave,apagar)):
                        itens_Liberados.append(chave)
                for apagaratual in apagar:
                    self.Lock_Table.pop(apagaratual)   
                
                
                print(f"C({commitExcluido}) efetuado!")
                self.liberar_itens_WaitQ(itens_Liberados, [commitExcluido])
            elif Aux==False:
                return
        
        commitado = len(self.CommitsEmEspera)
        
        while(commitado>0):
            
            for commitAtual in self.CommitsEmEspera:
                
                TR_Aux = self.tr_manager.buscar_TR_por_Id(commitAtual)
                if self.tr_manager.waitForDataList[TR_Aux][0] == 1:       
                    chaves = self.Lock_Table.keys()
                    itens_Liberados = []
                    apagar = []
                    for chave in chaves:
                        if(self.U(TR_Aux, chave,apagar)):
                            itens_Liberados.append(chave)
                    for apagaratual in apagar:
                        self.Lock_Table.pop(apagaratual)   
                    

                    print(f"C({commitAtual}) efetuado!")
                    
                    self.CommitsEmEspera.remove(commitAtual)
                    #Como foi commitado, o commit relativo à transação em questão é removido
                    
                    commitado += len(self.CommitsEmEspera)
                    #Isto é feito para que seja analisado se dá para commitar mais alguma transação depois da liberação desta

                    if(commitado>0):
                        print("Tentando executar operações de transações ativas em espera:")
                    
                    self.liberar_itens_WaitQ(itens_Liberados, [commitAtual])
                    
                    
                commitado -= 1
            


    def apagarTr(self, TR_Id):
        """Apaga as Transações de Tr da LockTable e verifica se operações de outras transações podem prosseguir"""
        self.Carregar_Lock_Table()    
        self.commitar(TR_Id)
        
        self.Escrever_Lock_Table()
        
        
    def controleOP(self, OP):
        #Função para avaliar a operação em relação ao bloqueio
        if OP.tipo[0] == 'B':
            print(f"BT{OP.item}-OK")
            #Neste caso, uma nova transação é iniciada
            Nova_Transacao = Transacao(OP.item,'Ativa',self.tr_manager.TS_Atual)
            
            self.tr_manager.inserir(Nova_Transacao)
            #Adiciona uma nova Transação na Tr_List com status ativa e depois aumenta o controle de tempo do Tr_Manager em um
            self.tr_manager.aumentar_TS()
        
        elif OP.tipo[0] == 'r':
            #Caso a função seja de Leitura, basta tentar chamar um bloqueio compartilhado. 
            print(f"r{OP.tipo[1]}({OP.item})-", end = '')

            TR = self.tr_manager.buscar_TR_por_Id(OP.tipo[1])
            self.LS(TR, OP.item)
        elif OP.tipo[0] == 'w':
            #Caso a função seja de Escrita, basta tentar chamar um bloqueio exclusivo.
            print(f"w{OP.tipo[1]}({OP.item})-", end = '')

            TR = self.tr_manager.buscar_TR_por_Id(OP.tipo[1])
            self.LX(TR, OP.item)
        else:
            #Só sobra a possibilidade de fim de transação.Basta verificar se a transação pode
            #ser liberada
            aux = False
            print(f"Iniciando o commit C{OP.item}")
            chaves = self.WaitQ.keys()
            for chave in chaves:
                Lock_aux = self.WaitQ[chave]
                while(Lock_aux!=None and aux==False):
                    if Lock_aux.TR_Id == OP.item :
                        self.printar_WaitQ()
                        print(f"C{OP.item} falhou(possui operacoes incompletas)\n")
                        aux = True
                    Lock_aux = Lock_aux.prox
            if aux == True:
                self.CommitsEmEspera.append(OP.item)
            else:
                self.apagarTr(OP.item)
        self.tr_manager.printarGrafo()
        

    def scheduler(self):
        print("Iniciando...\n")
        
        """
        Percorre a lista de OPS e executa a função controleOP para cada uma delas para que o controle de concorrência
        possa ser feito
        """
        for OP in self.OPS:
            self.controleOP(OP)
        
        print("História Finalizada!")