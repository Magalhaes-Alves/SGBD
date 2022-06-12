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
        self._serializavel = True
        self.tr_manager = Tr_Manager() 
    
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
        print('Gnt?')
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

        aux_Lock = self.Lock_Table[item]
        while(aux_Lock !=None):
            aux_Trans = self.tr_manager.buscar_TR_por_Id(aux_Lock.TR_Id)
            #Pega o TR e na linha seguinte pega a transação em si
            aux_Trans = self.tr_manager.get_TR(aux_Trans)

            if aux_Trans.Ts < trans_Enfileirada.Ts:
                trans_Enfileirada = aux_Trans
            count +=1
            aux_Lock = aux_Lock.prox
            
        if trans_Adicionada.TS > trans_Enfileirada.TS:
            print("ROLLBACK")

        if trans_Adicionada.Ts == trans_Enfileirada.Ts and count == 1 :
            print(f"Não entra aqui ?")
            self.Lock_Table[item].modo = Novo_Lock_Request.modo
        else:
            #Coloca na Lista de Espera
            if item in self.WaitQ.keys():
                print("Entra aqui?")
                #Coloca no final da lista de espera associada a este item
                aux_Lock = self.WaitQ[item]
                while aux_Lock.proximo != None:
                    aux_Lock = aux_Lock.prox
                aux_Lock.prox = Novo_Lock_Request
            else:
                print("Ou entra aqui?")
                self.WaitQ[item] = Novo_Lock_Request
        
        print("-"*20)
        


    def LS(self, TR, item):
        #insere um bloqueio no modo compartilhado na Lock_Table se puder,
		#senao insere um Lock_Request da transacao Tr na Wait_Q de D
        self.Carregar_Lock_Table()

        chaves = self.Lock_Table.keys()
        trans =(self.tr_manager.get_TR(TR))
        Novo_Lock_Request = Lock_Request("S", trans.Id,None, item)
        
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

        if (not item in chaves):
            #Significa que não há Pedido de bloqueio para este item
            self.Lock_Table[item] = Novo_Lock_Request
        else:
            #Senão , a página está bloqueada
            #Prevenção de Deadlock
            self.waitDie(TR, item, Novo_Lock_Request)
        
        
        self.Escrever_Lock_Table()

    def U(self, TR):
        """Apaga os bloqueios da transacao Tr da Lock_Table
	    Note que se existir mais de uma Transação bloqueando o item, ela permanecera bloqueada
        Percorre a Lock_Table desbloqueando a Transação TR"""

        #Percorre a Wait_Q apagando pedidos de Tr 
        chaves = self.Lock_Table.keys()

        for chave in chaves:
            request = self.WaitQ[chave]
            ant = request
            while(request != None):
                #Percorre toda a lista de LockRequests para um item da WaitQ
                TR_aux = self.tr_manager.buscar_TR_por_Id(request.TR_Id)
                if TR_aux == TR:
                    #Se a LockRequest daquela transação for a mesma da TR especificada para o desbloqueio
                    aux = request
                    if request == self.WaitQ[chave]:
                        if (chave in self.Lock_Table.keys()) and self.Lock_Table[chave].modo == 'X':
                            self.serializavel = False
                            return False
                        self.WaitQ[chave] = self.WaitQ[chave].prox
                        request = request.prox
                    else:
                        self.serializavel = False
                        #Lembrar de ver isso
                        ant.prox = request.prox
                        request = request.prox
                else:
                    ant = request
                    request = request.prox






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
            #Só sobra a possibilidade de fim de transação.Basta liberar a transação
            print(f"Iniciando o commit C{OP.item}\n")
            TR = self.tr_manager.buscar_TR_por_Id(OP.item)
            pass
        

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

