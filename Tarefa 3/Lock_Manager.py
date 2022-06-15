from Tr_Manager import Tr_Manager
from Transacao import Transacao
from Lock_Request import Lock_Request


class Lock_Manager():
    def __init__(self):
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
        #print("AQUI!\n\n")
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
        chaves = self.WaitQ.keys()
        print("""


        WAIT Q ,THIAGO


        """)
        for chave in chaves:
            aux = self.WaitQ[chave]
            while(aux != None):
                print(f"Item:{aux.item},Lock:{aux.modo},Tr_Id:{aux.TR_Id}\n")
                aux = aux.prox


    def waitDie(self,TR, item, Novo_Lock_Request):
        print("-"*20)
        print("Wait-Die:")
        trans_Adicionada = self.tr_manager.get_TR(TR)
        #Transação que ocasionou a execução do wait-die
        trans_Enfileirada = self.tr_manager.buscar_TR_por_Id(self.Lock_Table[item].TR_Id)
        #Pega o TR e na linha seguinte pega a transação em si
        trans_Enfileirada = self.tr_manager.get_TR(trans_Enfileirada)

        count = 0
        countRoll = 0

        aux_Lock = self.Lock_Table[item]
        while(aux_Lock !=None):
            aux_Trans = self.tr_manager.buscar_TR_por_Id(aux_Lock.TR_Id)
            #Pega o TR e na linha seguinte pega a transação em si
            aux_Trans = self.tr_manager.get_TR(aux_Trans)

            if trans_Adicionada.Ts < aux_Trans.Ts:
                countRoll = 1   
            count +=1
            aux_Lock = aux_Lock.prox
            
        if countRoll>0:
            print("ROLLBACK")

        if trans_Adicionada.Ts == trans_Enfileirada.Ts and count == 1 :
            self.Lock_Table[item].modo = Novo_Lock_Request.modo
        else:
            #Coloca na Lista de Espera
            if item in self.WaitQ.keys():
                
                #Coloca no final da lista de espera associada a este item
                aux_Lock = self.WaitQ[item]
                while aux_Lock.prox != None:
                    aux_Lock = aux_Lock.prox
                aux_Lock.prox = Novo_Lock_Request
            else:
                
                self.WaitQ[item] = Novo_Lock_Request
        
        print("-"*20)
        


    def LS(self, TR, item):
        #insere um bloqueio no modo compartilhado na Lock_Table se puder,
		#senao insere um Lock_Request da transacao Tr na Wait_Q de D
        self.Carregar_Lock_Table()

        chaves = self.Lock_Table.keys()
        trans =(self.tr_manager.get_TR(TR))
        Novo_Lock_Request = Lock_Request("S", trans.Id,None, item)
        
        #Será que a transação em questão está com uma operação anterior em espera?
        chaves2 = self.WaitQ.keys()
        for chave in chaves2:
            Lock_aux = self.WaitQ[chave]

            while(Lock_aux!=None):
                if(Lock_aux.TR_Id == trans.Id):
                    #Há uma operação da mesma transação em espera, então ela deve entrar em espera
                    if item in chaves2:
                        Lock_aux = self.WaitQ[item]
                        while(Lock_aux.prox!=None):
                            Lock_aux = Lock_aux.prox
                        Lock_aux.prox = Novo_Lock_Request
                    else:
                        self.WaitQ[item] = Novo_Lock_Request
                    
                    self.Escrever_Lock_Table()
                    return

                Lock_aux =Lock_aux.prox


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

        chaves2 = self.WaitQ.keys()
        for chave in chaves2:
            Lock_aux = self.WaitQ[chave]

            while(Lock_aux!=None):
                if(Lock_aux.TR_Id == trans.Id):
                    #Há uma operação da mesma transação em espera, então ela deve entrar em espera
                    if item in chaves2:
                        Lock_aux = self.WaitQ[item]
                        while(Lock_aux.prox!=None):
                            Lock_aux = Lock_aux.prox
                        Lock_aux.prox = Novo_Lock_Request
                    else:
                        self.WaitQ[item] = Novo_Lock_Request
                    
                    self.Escrever_Lock_Table()
                    return

                Lock_aux =Lock_aux.prox

        if (not item in chaves):
            #Significa que não há Pedido de bloqueio para este item
            self.Lock_Table[item] = Novo_Lock_Request
        else:
            #Senão , a página está bloqueada
            #Prevenção de Deadlock
            self.waitDie(TR, item, Novo_Lock_Request)
        
        
        self.Escrever_Lock_Table()

    def U(self, TR, item):
        """Apaga os bloqueios da transacao Tr em relação a determinado item da Lock_Table"""

        trans = self.tr_manager.get_TR(TR)
        
        Corrente = self.Lock_Table[item]
        saida = False

        Anterior = None
        while (Corrente != None):
            Seguinte = Corrente.prox
            if trans.Id == Corrente.TR_Id:
                if Anterior == None:
                    Corrente = Corrente.prox
                elif Seguinte == None:
                    Anterior.prox = None
                else:
                    Anterior.prox = Corrente.prox
                saida = True
            Anterior = Corrente
            Corrente = Corrente.prox

        
        if(self.Lock_Table[item]==None):
            self.Lock_Table.pop(item)

        
        return saida

    def UWaitQ(self, item):
        pass

    def apagarTr(self, TR_Id):
        """Apaga as Transações de Tr da LockTable e verifica se operações de outras transações podem prosseguir"""
        self.Carregar_Lock_Table()
        print("TESTE DE CORNO1:")
        self.Printar_Lock_Table()
        TR = self.tr_manager.buscar_TR_por_Id(TR_Id)
        chaves = self.Lock_Table.keys()
        itens_Liberados = []

        for chave in chaves:
            if(self.U(TR, chave)):
                itens_Liberados.append(chave)
            

        chaves = self.Lock_Table.keys()
        chaves2 = self.WaitQ.keys()
        
        for item_liberado in itens_Liberados:
            #Verifica se a WaitQ tem Transacoes associadas ao item que foi liberado
            chaves2 = self.WaitQ.keys()
            if item_liberado in chaves2:
                #Se há transações associadas a esse item na lista de Espera.O primeiro bloqueio
                #da lista de espera é pego
                Lock_aux = self.WaitQ[item_liberado]
        
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
        

    def scheduler(self, OPS):
        print("Iniciando...\n")
        
        """
        Percorre a lista de OPS e executa a função controleOP para cada uma delas para que o controle de concorrência
        possa ser feito
        """
        for OP in OPS:
            self.controleOP(OP)

            if(not self.serializavel):
                print("Esta história não é serializável")
                break
        self.printar_WaitQ()
        print(f"""
        {self.CommitsEmEspera}
        """)

