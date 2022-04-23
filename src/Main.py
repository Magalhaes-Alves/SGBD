



with open("in.txt",'r') as entrada, open("out.txt",'w') as saida, open("diretorio.txt","r") as diretorio:
    comandos = entrada.readlines()

    for op in comandos:
        operacao = op
        operacao.split(':')
        if operacao[0][0:3]== "INC":
            #Fazer inclusão
            pass
        elif operacao[0][0:3]== "REM":
            #Fazer remoção
            pass
        elif operacao[0][0:2]== "BUS":
            #Fazer busca
            pass
        else:
            pass
        
    