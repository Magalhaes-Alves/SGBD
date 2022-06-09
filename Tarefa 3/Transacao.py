class Transacao():
    def __init__(self, Id, status, Ts):
        self._Id = Id
        self._status = status
        self._Ts = Ts

    @property
    def Id(self):
        return self._Id

    @property
    def Ts(self):
        return self._Ts

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status):
        self._status = status

