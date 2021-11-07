from utils import *

class Shingle:
    """
    Set of hashed shingles for a document
    """
    def __init__(self, k:int, docId: int):
        self.k = k #number of chars in a single shingle
        self.shingle_set = set()
        self.docId = docId
        self.hash_fn = hashFamily(100) 

    def createShingles(self, doc:list):
        """Take the shingles

        Args:
            doc (list): list of tokens in the description field of the document

        Raises:
            ValueError: If the description, for some reason, is shorter than 10 chars, print an error message
        """
        text = ' '.join(doc)
        self.doc_len = len(text)
        if(self.doc_len < self.k): #Some descriptions could be too short
            raise ValueError("!-------Document %s is too short to create a shingle-------!" %(self.docId))
        for i in range(self.doc_len - self.k +1): 
            doc_shingle = text[i:i+self.k]
            encoded_shingle = str(doc_shingle.encode("utf-8", "strict")) #encoding is needed to hash the shingle
            self.shingle_set.add(self.hash_fn(encoded_shingle))

    def __str__(self) ->str:
        return "Shingles for the doc: %s are: %s"%(self.docId, self.shingle_set)
