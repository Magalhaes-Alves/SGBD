from Lock_Manager import Lock_Manager
from Operation import Operation

def Carregar_Ops(op_lida, fator,cont):
    if(op_lida[0] == 'B'):
        tipo = 'BT'
    elif(op_lida[0] == 'C'):
        tipo = 'C'
    else:
        tipo = op_lida[:op_lida.find('(')]
    item = op_lida[op_lida.find('(') + 1: -fator]
    op_aux = Operation(cont, tipo, item)
    
    return op_aux


arq = open('in.txt', 'r')
ops_lidas = arq.readlines()
arq.close()

OPS = []
lm = Lock_Manager()
cont = 0

"""
Este teste é para saber se todos os comandos do in.txt estão em apenas uma linha ou se a formatação é um comando por linha.
Outros padrões não serão aceitos.

O teste consistente basicamente de ver quantos '(' há na primeira string após o readlines().
"""


if ops_lidas[0].count('(') > 1:
    ops_lidas = ops_lidas[0].split(')')[:-1]
    
    for op_lida in ops_lidas[:-1]:
        op_aux = Carregar_Ops(op_lida, -len(op_lida), cont)
        cont += 1
        OPS.append(op_aux)
    
    op_lida = ops_lidas[-1]
    if(op_lida[-1] == '\n'):
        op_aux = Carregar_Ops(op_lida, -len(op_lida)+1, cont)
    else:
        op_aux = Carregar_Ops(op_lida, -len(op_lida), cont)

    OPS.append(op_aux)
else:
    for op_lida in ops_lidas[:-1]:
        op_aux = Carregar_Ops(op_lida, 2, cont)
        cont += 1
        OPS.append(op_aux)
    
    op_lida = ops_lidas[-1]
    if(op_lida[-1] == '\n'):
        op_aux = Carregar_Ops(op_lida, 2, cont)
    else:
        op_aux = Carregar_Ops(op_lida, 1, cont)

    OPS.append(op_aux)

lm.scheduler(OPS)

"""for algo in OPS:
    print(f"Id:{algo.id},tipo:{algo.tipo},item:{algo.item}")"""

