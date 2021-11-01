from utils import *

class Shingle:
    def __init__(self, k:int, docId: int):
        self.k = k
        self.shingle_set = set()
        self.docId = docId
        self.hash_fn = hashFamily(32)

    def createShingles(self, doc:list):
        text = ' '.join(doc)
        self.doc_len = len(text)

        for i in range(self.doc_len - self.k +1): #some announcements are too short -> handle this case somehow
            doc_shingle = text[i:i+self.k]
            encoded_shingle = str(doc_shingle.encode("utf-8", "strict"))
            self.shingle_set.add(self.hash_fn(encoded_shingle))

    def __str__(self) ->str:
        return "Shingles for the doc: %s are: %s"%(self.docId, self.shingle_set)

class Jaccard:
    def __init__(self, set1:Shingle, set2:Shingle):
        self.set1 = set1.shingle_set
        self.set2 = set2.shingle_set
        self.union = self.set1 | self.set2
        self.intersection = self.set1 & self.set2
        self.jaccard = len(self.intersection) / len(self.union)

    def __str__(self):
        return "The Jaccard similarity between the two sets is: %s" %(self.jaccard)

    def printJaccard(self):
        print("Union between set1 and set2 is: {}, intersection is: {} -> Jaccard similarity is: {}".format(self.union, self.intersection, self.jaccard))