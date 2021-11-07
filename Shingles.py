from utils import *

class Shingle:
    def __init__(self, k:int, docId: int):
        self.k = k
        self.shingle_set = set()
        self.docId = docId
        self.hash_fn = hashFamily(100)

    def createShingles(self, doc:list):
        text = ' '.join(doc)
        self.doc_len = len(text)
        if(self.doc_len < self.k): #Some descriptions could be too short
            raise ValueError("!-------Document %s is too short to create a shingle-------!" %(self.docId))
        for i in range(self.doc_len - self.k +1): #some announcements are too short -> handle this case somehow
            doc_shingle = text[i:i+self.k]
            encoded_shingle = str(doc_shingle.encode("utf-8", "strict"))
            self.shingle_set.add(self.hash_fn(encoded_shingle))

    def __str__(self) ->str:
        return "Shingles for the doc: %s are: %s"%(self.docId, self.shingle_set)
