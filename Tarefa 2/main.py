# VOCE DEVE INCLUIR SUAS IMPORTACOES AQUI, CASO NECESSARIO!!!
from Tabela import Tabela
from Operador import Operador


def main():
    vinho = Tabela("vinho.csv") # cria estrutura necessaria para a tabela
    uva = Tabela("uva.csv")
    pais = Tabela("pais.csv")
    
    vinho.carregarDados() # le os dados do csv e add na estrutura da tabela, caso necessario
    uva.carregarDados()
    pais.carregarDados()
        
    ## DESCOMENTE A PROXIMA LINHA CASO SEU TRABALHO SEJA SELECAO:
    # op = Operador(vinho, ["ano_colheita", "uva_id"], ["1990", "0"])
    ## significa: SELECT * FROM Vinho WHERE ano_colheita = '1990' AND uva_id = '0'
    ## IMPORTANTE: isso eh so um exemplo, pode ser outra tabela e ter mais ou menos colunas/constantes.
    ## genericamente: Operador(tabela, lista_colunas, lista_constantes): 
    ## significa: SELECT * FROM tabela WHERE col_1 = con_1 AND col_2 = con_2 AND ... AND col_n = con_n

    ## DESCOMENTE A PROXIMA LINHA CASO SEU TRABALHO SEJA PROJECAO:
    # op = Operador(vinho, ["uva_id", "rotulo"]) 
    ## significa: SELECT uva_id, rotulo FROM Vinho
    ## IMPORTANTE: isso eh so um exemplo, pode ser outra tabela e ter mais ou menos colunas.
    ## genericamente: Operador(tabela, lista_colunas_proj):
    ## significa: SELECT col_1, col_2, ..., col_n FROM tabela

    ## DESCOMENTE A PROXIMA LINHA CASO SEU TRABALHO SEJA JUNCAO:
    op = Operador(vinho, uva, "vinho_id", "uva_id")
    ## significa: SELECT * FROM Vinho V, Uva U WHERE V.vinho_id = U.uva_id
    ## IMPORTANTE: isso eh so um exemplo, pode ser tabelas/colunas distintas.
    ## genericamente: Operador(tabela_1, tabela_2, col_tab_1, col_tab_2):
    ## significa: SELECT * FROM tabela_1, tabela_2 WHERE col_tab_1 = col_tab_2

    op.executar() # Realiza a operacao desejada
    
    print("#Pags:", op.numPagsGeradas()) # Retorna a quantidade de paginas geradas pela operacao
    print("#IOss:", op.numIOExecutados()) # Retorna a quantidade de IOs geradas pela operacao
    print("#Tups:", op.numTuplasGeradas()) # Retorna a quantidade de tuplas geradas pela operacao
    
    op.salvarTuplasGeradas("selecao_vinho_ano_colheita_1990.csv") # Retorna as tuplas geradas pela operacao e salva em um csv

    #Abaixo está uma função simples só para excluir tudo relacionado aos arquivos de uma operação(paginas,diretorio,buckets do hash,paginas de saida e afins)
    #Para rodar de uma operação para outra sugiro executar dnv a operação abaixo descomentada para tornar menos poluido, deixando a correção mais fácil
    #op.excluirParaCorrecao(vinho, uva, pais)

    #A seguir será colocado alguns exemplos.Para rodá-los, basta descomentar as linhas e comentar as respectivas linhas acima
    """op = Operador(vinho, uva, "uva_id", "uva_id")
    op.executar()
    print("#Pags:", op.numPagsGeradas())
    print("#IOss:", op.numIOExecutados())
    print("#Tups:", op.numTuplasGeradas())
    op.salvarTuplasGeradas("exemplo1.csv")"""

    #Só para reforçar, para usar o excluir acima, basta rodar esse bloco de operações dnv com a operação de excluir descomentada
    # (é bem ruim pq tem que rodar tudo dnv, mas foi o que deu para fazer)
    #op.excluirParaCorrecao(vinho, uva, pais)

    """op = Operador(vinho, pais, "vinho_id", "pais_id")
    op.executar()
    print("#Pags:", op.numPagsGeradas())
    print("#IOss:", op.numIOExecutados())
    print("#Tups:", op.numTuplasGeradas())
    op.salvarTuplasGeradas("exemplo2.csv")"""
    #op.excluirParaCorrecao(vinho, uva, pais)

main()