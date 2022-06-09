from Tr_Manager import Tr_Manager
from Transacao import Transacao
from Lock_Request import Lock_Request


class Lock_Manager():
    def __init__(self):
        self._Lock_Table = {}
        """
        Nesta implementação será usada a representação de um grafo por lista de adjacências, ou seja, Lock_Table[Tr]
        é a lista de adjacências relativa à Transação Tr(número descrito no enunciado).
        Isto funciona devido ao ponteiro para próximo na classe Lock_Request, já que basta fazer operações relativas
        a uma lista de adjacências para manipula-lá.Assim, o grafo de transações fica mais simples.
        
        Caso,não haja elemento correspondente a uma chave Tr no dicionário Lock_Table, simplesmente significa que 
        a Transação Tr não tem arestas no grafo de Transações.
        """

        with open('Lock_Table.txt', 'w') as arq:
            arq.write("Item,Lock,Tr_Id\n")

        self.WaitQ = {}
        self._serializavel = True
        self.tr_manager = Tr_Manager() 
    
    @property
    def serializavel(self):
        return self._serializavel
    
    @property
    def Lock_Table(self):
        return self._Lock_Table


    def Carregar_Lock_Table(self):
        arq = open('Lock_Table.txt', 'r')
        registros = arq.readlines()
        arq.close()

        for registro in registros[1:]:
            atributos = registro.split(',')
            TR = self.tr_manager.buscar_TR_por_Id(atributos[2])
            Novo_Lock_Request = Lock_Request(atributos[1], TR, None, atributos[0])

            chaves = self.Lock_Table.keys()
            if TR in chaves:
                "Coloca no final da Lista de Adjacências"
                aux = self.Lock_Table[TR]
                while(aux.prox != None):
                    aux = aux.prox
                aux.prox = Novo_Lock_Request
            else:
                "Cria a lista de Adjacências para esta transação"
                self.Lock_Table[TR] = Novo_Lock_Request
        

    def Printar_Lock_Table(self):
        #print("AQUI!\n\n")
        chaves = self.Lock_Table.keys()
        for chave in chaves:
            aux = self.Lock_Table[chave]
            Id_TR = self.tr_manager.get_TR(aux.TR).Id
            while(aux != None):
                print(f"Item:{aux.item},Lock{aux.modo},Tr_Id:{Id_TR}")
                aux = aux.prox


    def Escrever_Lock_Table(self):
        chaves = self.Lock_Table.keys()
        arq = open('Lock_Table.txt', 'w')
        arq.write("Item,Lock,Tr_Id\n")
        
        for chave in chaves:
            aux = self.Lock_Table[chave]
            Id_TR = self.tr_manager.get_TR(aux.TR).Id
            while(aux != None):
                arq.write(f'{aux.Item},{aux.modo},{Id_TR}\n')
        
        arq.close()


    def LS(self, TR, item):
        #insere um bloqueio no modo compartilhado na Lock_Table se puder,
		#senao insere um Lock_Request da transacao Tr na Wait_Q de D
        self.Carregar_Lock_Table()

        Novo_Lock_Request = Lock_Request("S", TR, None, item)
        chaves = self.Lock_Table.keys()

        if (not TR in chaves):
            #Significa que não há Pedido de bloqueio para esta transação
            self.Lock_Table[TR] = Novo_Lock_Request
        elif self.Lock_Table[TR].modo == 'S':
            """Se o bloqueio for do tipo compartilhado, adiciona transação como uma das que bloqueia a Transação"""
        self.Printar_Lock_Table()
        

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
            
            TR = self.tr_manager.buscar_TR_por_Id(OP.tipo[1])
            print(f"Id da transação:{OP.tipo[1]} | Leitura do item:{OP.item}")
            print(f"TR da Transação de id {OP.tipo[1]}:{TR}\n")
            self.LS(TR, OP.item)


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
        self.tr_manager.Printar_Tr_Manager()

"""lm = Lock_Manager()
with open("Lock_Table.txt",'a') as arq:
    arq.write('x,S,1\n')
    arq.write('y,X,2\n')
    arq.write('x,S,2\n')

lm.Carregar_Lock_Table()
lm.Printar_Lock_Table()
"""