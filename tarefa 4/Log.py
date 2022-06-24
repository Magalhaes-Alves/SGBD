
#Essa classe irá armazenar totas as historias 
class Log:

    def __init__(self,arquivo):

        with open(arquivo, 'r') as historias:
            self._log = historias.readlines()
            self._log = list(map(lambda x: x[2:-3].split(' | '),self._log))

    def mostrarLog(self):
        for i in range(len(self._log)):
            print(f'[{self._log[i]}]\n')


