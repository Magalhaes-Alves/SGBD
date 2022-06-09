class Operation():
    def __init__(self, id, tipo, item):
        self._id = id
        self._tipo = tipo
        self._item = item
    
    @property
    def id(self):
        return self._id

    @property
    def tipo(self):
        return self._tipo

    @property
    def item(self):
        return self._item