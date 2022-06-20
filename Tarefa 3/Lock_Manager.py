from Tr_Manager import Tr_Manager
from Transacao import Transacao
from Lock_Request import Lock_Request


class Lock_Manager():
    def __init__(self, OPS):
        self._Lock_Table = {}
        """
        Neste dicionário, a chave é o item e o valor relativo a uma chave é a lista de Lock_Requests associados àquele item.
        Esta lista é percorrida a partir do ponteiro para próximo.
        """

        with open('Lock_Table.txt', 'w') as arq:
            arq.write("Item,Lock,Tr_Id\n")

        self._WaitQ = {}
        self._CommitsEmEspera = []
        self._serializavel = True
        self.tr_manager = Tr_Manager()
        self._OPS = OPS
        self._OPS_Postergadas = {}

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
    def serializavel(self):
        return self._serializavel
    
    @serializavel.setter
    def serializavel(self, novo):
        self._serializavel = novo

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


    def postergarTR(self,Lock_Request_Aux):
        TR_ID = Lock_Request_Aux.TR_Id
        modo = 'r' if Lock_Request_Aux.modo == 'S' else 'w'
        item = Lock_Request_Aux.item
        TR_aux = self.tr_manager.buscar_TR_por_Id(TR_ID)
        self.OPS_Postergadas[TR_ID] = []

        i = 0
        while(self.OPS[i].tipo[0] != modo or self.OPS[i].tipo[1] != TR_ID or self.OPS[i].item !=item):
            #Iterar sobre a lista de operações até a operação atual
            if((self.OPS[i].tipo[0] ==  'r' or self.OPS[i].tipo[0] ==  'w') and self.OPS[i].tipo[1] == TR_ID):
                print(f"Tipo:{self.OPS[i].tipo[0]}, item:{self.OPS[i].item}, TR_ID:{self.OPS[i].tipo[1]}")
                
                self.OPS_Postergadas[TR_ID].append((self.OPS[i]))
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
                        if TR_ID == Corrente.TR_Id:                
                            if Anterior == None:
                                self.Lock_Table[self.OPS[i].item] = Corrente.prox
                                Anterior = None
                            elif Seguinte == None:
                                Anterior.prox = None
                                Anterior = Corrente
                            else:
                                Anterior.prox = Corrente.prox
                                Anterior = Corrente
                            verificaWait = False
                        Corrente = Corrente.prox

                    if(self.Lock_Table[self.OPS[i].item]==None):
                        self.Lock_Table.pop(self.OPS[i].item)
                
                #Procurar na WaitQ
                if verificaWait==True:
                    Corrente = self.WaitQ[self.OPS[i].item]

                    Anterior = None
                    while (Corrente != None):
                        Seguinte = Corrente.prox
                        if TR_ID.Id == Corrente.TR_Id:                
                            if Anterior == None:
                                self.WaitQ[self.OPS[i].item] = Corrente.prox
                                Anterior = None
                            elif Seguinte == None:
                                Anterior.prox = None
                                Anterior = Corrente
                            else:
                                Anterior.prox = Corrente.prox
                                Anterior = Corrente
                            break
                        Corrente = Corrente.prox

                    if(self.WaitQ[self.OPS[i].item]==None):
                        self.WaitQ.pop(self.OPS[i].item)
            
            i+=1
        
        self.OPS_Postergadas[TR_ID].append(self.OPS[i])
        self.tr_manager.waitForDataList[TR_aux] = [-1]


    def rollBack(self, transacao,Lock_Request_Postergado):
        #Deve-se colocar as operações relativas a trans_Adicionada na fila de transações postergadas
        self.postergarTR(Lock_Request_Postergado)
        itensLiberados = []
        for operacao in self.OPS_Postergadas[transacao.Id]:
            itensLiberados.append(operacao.item)
        
        #Deve-se tentar executar operações de transações ativas em espera.Caso alguma transação seja commitada
        #neste proccesso, deve-se tentar executar novamente operações de transações ativas em espera.
        
        apagar = []
        self.liberar_itens_WaitQ(itensLiberados,apagar)
        for apagaratual in apagar:
            self.WaitQ.pop(apagaratual)
        self.ajustar_WaitforData()

        self.printar_WaitQ()
        self.Printar_Lock_Table()
        self.commitar()
        
        #Finalmente, deve-se tentar reiniciar as transações de acordo com sua ordem na fila de transações postergadas
        self.Escrever_Lock_Table()
        TR_Topo = list(self.OPS_Postergadas.keys())[0]

        TR_aux = self.tr_manager.buscar_TR_por_Id(TR_Topo)
        for operacao in self.OPS_Postergadas[TR_Topo]:
            if operacao.tipo[0] == 'r':
                self.LS(TR_aux,operacao.item)
            else:
                self.LX(TR_aux,operacao.item)
        
        if TR_Topo in self.CommitsEmEspera:
            self.commitar()
        
        self.OPS_Postergadas.pop(TR_Topo)
        self.Carregar_Lock_Table()

    def waitDie(self,TR, item, Novo_Lock_Request):

        trans_Adicionada = self.tr_manager.get_TR(TR)
        #Transação que ocasionou a execução do wait-die
        trans_Enfileirada = self.tr_manager.buscar_TR_por_Id(self.Lock_Table[item].TR_Id)
        #Pega o TR e na linha seguinte pega a transação em si
        trans_Enfileirada = self.tr_manager.get_TR(trans_Enfileirada)

        count = 0

        aux_Lock = self.Lock_Table[item]
        while(aux_Lock !=None):
            aux_Trans = self.tr_manager.buscar_TR_por_Id(aux_Lock.TR_Id)
            #Pega o TR e na linha seguinte pega a transação em si
            aux_Trans = self.tr_manager.get_TR(aux_Trans)

            if trans_Adicionada.Ts > aux_Trans.Ts and aux_Lock.modo == 'X':
                #A transação de trans_Adicionada deve ser postergada devido a uma situação de ROLLBACK
                print(f"RollBack TS({trans_Adicionada.Id})<TS({aux_Trans.Id})")
                self.rollBack(trans_Adicionada, Novo_Lock_Request)
                return

            count += 1
            aux_Lock = aux_Lock.prox
            

        if trans_Adicionada.Ts == trans_Enfileirada.Ts and count == 1:
            #Isto significa que a operação que ocasionou a execução do waitDie é a mesma
            #do único bloqueio ques está na LockTable.Sendo assim, este novo Bloqueio é adicionado
            #à LockTable
            self.Lock_Table[item].modo = Novo_Lock_Request.modo
            self.Lock_Table[item].prox = Novo_Lock_Request
        else:
            #Coloca na Lista de Espera
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
        
        
        

    def woundWait(self,TR, item, Novo_Lock_Request):
        pass


    def LS(self, TR, item):
        #insere um bloqueio no modo compartilhado na Lock_Table se puder,
		#senao insere um Lock_Request da transacao Tr na Wait_Q de D
        self.Carregar_Lock_Table()

        chaves = self.Lock_Table.keys()
        trans =(self.tr_manager.get_TR(TR))
        Novo_Lock_Request = Lock_Request("S", trans.Id,None, item)
        
        #Será que a transação em questão está com uma operação anterior em espera?
        if self.tr_manager.waitForDataList[TR][0] == 0:
            self.tr_manager.waitForDataList[TR].append(item)

        if (not item in chaves):
            #Significa que não há Pedido de bloqueio para este item
            self.Lock_Table[item] = Novo_Lock_Request
        elif self.Lock_Table[item].modo == 'S':
            """Se o bloqueio for do tipo compartilhado, adiciona transação como uma das que bloqueia o item"""
            aux = self.Lock_Table[item]
            while(aux.prox !=None):
                aux = aux.prox
            aux.prox = Novo_Lock_Request
        else:
            #Situação em que self.Lock_Table[item].modo == 'D'
            self.waitDie(TR, item, Novo_Lock_Request)

        
        self.Escrever_Lock_Table()

    def LX(self, TR, item):
        #Insere um bloqueio no modo exclusivo na Lock_Table
        self.Carregar_Lock_Table()

        trans = self.tr_manager.get_TR(TR)
        chaves = self.Lock_Table.keys()
        Novo_Lock_Request = Lock_Request("X", trans.Id,None, item)

        #Será que a transação em questão está com uma operação anterior em espera?
        if self.tr_manager.waitForDataList[TR][0] == 0:
            self.tr_manager.waitForDataList[TR].append(item)

        if (not item in chaves):
            #Significa que não há Pedido de bloqueio para este item
            self.Lock_Table[item] = Novo_Lock_Request
        else:
            #Senão , a página está bloqueada
            #Prevenção de Deadlock
            self.waitDie(TR, item, Novo_Lock_Request)
        
        
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
                    Anterior = None
                elif Seguinte == None:
                    Anterior.prox = None
                    Anterior = Corrente
                else:
                    Anterior.prox = Corrente.prox
                    Anterior = Corrente
                saida = True
            Corrente = Corrente.prox

        
        if(self.Lock_Table[item]==None):
            apagar.append(item)

        
        return saida

    def liberar_itens_LockTable(self):
        pass
    

    def ajustar_WaitforData(self):
        #Função para passar por todas as Listas de esperas das transações após a liberação de itens da WaitQ
        #para verificar se os itens na WaitForDataLista são de operações que estão na LockTable e apenas estavam em espera
        chaves = self.tr_manager.waitForDataList.keys()
        chaves2 = self.WaitQ.keys()
        for chave in chaves:
            listaTR = self.tr_manager.waitForDataList[chave]
            controle = 0
            #Variável para contar quantas operações na WaitForDataList estão em espera por bloqueio de outra Transação
            for item in listaTR[1:]:
                if item in chaves2:
                    #Se há Lista de espera associada ao item, verifica se a transação em questão tem operações nessa waitQ
                    # que estão em espera devido a um bloqueio na lockTable
                    TR_Id_aux = self.tr_manager.get_TR(chave).Id
                    WaitQ_aux = self.WaitQ[item]
                    while(WaitQ_aux!=None):
                        if(WaitQ_aux.TR_Id == TR_Id_aux):
                            controle +=1
                        WaitQ_aux = WaitQ_aux.prox
            if(controle==0):
                self.tr_manager.waitForDataList[chave] = [1]
                
                

    def liberar_itens_WaitQ(self, itens_Liberados,apagar):
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
                        print(f"TR_ID:{TR_Id_Aux},Corrente.TR_Id:{Corrente.TR_Id}")
                        aux_Excluir = Corrente
                        #Apagar o Bloqueio em questão da WaitQ   
                        if Anterior == None:
                            print("TESTE 1")
                            self.WaitQ[item_liberado] = Corrente.prox
                            Anterior = None
                        elif Seguinte == None:
                            print("TESTE 2")
                            Anterior.prox = None
                            Anterior = Corrente
                        else:
                            print("TESTE 3")
                            Anterior.prox = Corrente.prox
                            Anterior = Corrente
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

                    Corrente = Corrente.prox
                if(self.WaitQ[item_liberado]==None):
                    apagar.append(item_liberado)



    def commitar(self):
        commitado = len(self.CommitsEmEspera)
        #Variável para entrar no loop a seguir e saber se alguma Transação foi commitada

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
                    apagar = []    
                    

                    self.liberar_itens_WaitQ(itens_Liberados,apagar)
                    for apagaratual in apagar:
                        self.WaitQ.pop(apagaratual)
                    apagar = [] 
                    self.ajustar_WaitforData()

                    self.CommitsEmEspera.remove(commitAtual)
                    #Como foi commitado, o commit relativo à transação em questão é removido
                    commitado += len(self.CommitsEmEspera)
                    #Isto é feito para que seja analisado se dá para commitar mais alguma transação depois da liberação desta
                commitado -=1


    def apagarTr(self, TR_Id):
        """Apaga as Transações de Tr da LockTable e verifica se operações de outras transações podem prosseguir"""
        self.Carregar_Lock_Table()

        TR = self.tr_manager.buscar_TR_por_Id(TR_Id)
        chaves = self.Lock_Table.keys()
        itens_Liberados = []
        apagar = []
        for chave in chaves:
            if(self.U(TR, chave,apagar)):
                itens_Liberados.append(chave)
        for apagaratual in apagar:
            self.Lock_Table.pop(apagaratual)
        apagar = []
        
        self.liberar_itens_WaitQ(itens_Liberados,apagar)
        for apagaratual in apagar:
            self.WaitQ.pop(apagaratual)
        apagar = [] 
        self.ajustar_WaitforData()
        
        #Commita o que foi apagado
        self.commitar()
        
        
        print("WaitQ")
        self.printar_WaitQ()
        self.Escrever_Lock_Table()
        

    def controleOP(self, OP):
        #Função para avaliar a operação em relação ao bloqueio
        if OP.tipo[0] == 'B':
            print(f"Iniciando a Transação T{OP.item}\n")
            #Neste caso, uma nova transação é iniciada
            Nova_Transacao = Transacao(OP.item,'Ativa',self.tr_manager.TS_Atual)
            
            self.tr_manager.inserir(Nova_Transacao)
            #Adiciona uma nova Transação na Tr_List com status ativa e depois aumenta o controle de tempo do Tr_Manager em um
            self.tr_manager.aumentar_TS()
        
        elif OP.tipo[0] == 'r':
            #Caso a função seja de Leitura, basta tentar chamar um bloqueio compartilhado. 
            print("Read -")

            TR = self.tr_manager.buscar_TR_por_Id(OP.tipo[1])
            print(f"Id da transação:{OP.tipo[1]} | Leitura do item:{OP.item}")
            print(f"TR da Transação de id {OP.tipo[1]}:{TR}\n")
            self.LS(TR, OP.item)
        elif OP.tipo[0] == 'w':
            #Caso a função seja de Escrita, basta tentar chamar um bloqueio exclusivo.
            print("Write -")

            TR = self.tr_manager.buscar_TR_por_Id(OP.tipo[1])
            print(f"Id da transação:{OP.tipo[1]} | Leitura do item:{OP.item}")
            print(f"TR da Transação de id {OP.tipo[1]}:{TR}\n")
            self.LX(TR, OP.item)
        else:
            #Só sobra a possibilidade de fim de transação.Basta verificar se a transação pode
            #ser liberada
            print(f"Iniciando o commit C{OP.item}\n")
            chaves = self.WaitQ.keys()
            for chave in chaves:
                Lock_aux = self.WaitQ[chave]
                while(Lock_aux!=None):
                    if Lock_aux.TR_Id == OP.item :
                        print(f"C{OP.item} falhou(possui operacoes incompletas)\n")
                        self.CommitsEmEspera.append(OP.item)
                        return
                    Lock_aux = Lock_aux.prox
            
            self.apagarTr(OP.item)
        

    def scheduler(self):
        print("Iniciando...\n")
        
        """
        Percorre a lista de OPS e executa a função controleOP para cada uma delas para que o controle de concorrência
        possa ser feito
        """
        for OP in self.OPS:
            self.controleOP(OP)

            if(not self.serializavel):
                print("Esta história não é serializável")
                break

