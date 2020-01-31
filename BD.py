#dicionario dentro do dicionario
class BD:
    def __init__(self):
        self.BD = {} 
           
    def setSeq(self, seq, id):
        if self.VerificaID(id) == False:
            self.BD[id] = seq #insere no dicionario a nova sequencia
            return True
        else:
            return False
    
    def getKeys(self):
        return self.BD.keys()
    
    def getBD(self):
        return self.BD

    def getSeq(self, id): #falta meter a verificar o id
        return self.BD.get(id)
    
    def getSeqs(self):
        return self.BD.values()

    def VerificaID(self, id): # VERIFICA SE O ID JA EXISTE
        if id in self.BD:
            return True
        else:
            return False
        
        