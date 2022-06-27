from Log import Log

class Recuperacao:
    

    def __init__(self, nome_arquivo_log ):

        self._log = Log(nome_arquivo_log)
        print(self._log.extrairTransacoes())
        print(self._log.extraiObjetos())
        self._undo =[]
        self._objetos = self._log.extraiObjetos()

