
class DB:
    def __init__(self):
        self.DB = {} 
           
    def setSeq(self, seq, id):
        if self.VerifyID(id) == False:
            self.DB[id] = seq #insers in a dictionary type of database the new sequence
            return True
        else:
            return False
    
    def getKeys(self):
        return self.DB.keys()
    
    def getDB(self):
        return self.DB

    def getSeq(self, id): 
        return self.DB.get(id)
    
    def getSeqs(self):
        return self.DB.values()

    def VerifyID(self, id): # Verifies if the iD already exits
        if id in self.DB:
            return True
        else:
            return False
        
        