from Tr_Manager import Tr_Manager

class Lock_Manager():
    def __init__(self):
        self.Lock_Table = []
        with open('Lock_Table.txt', 'w'):
            pass

        self.WaitQ = {}
        self.tr_manager = Tr_Manager() 

    