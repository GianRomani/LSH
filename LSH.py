from utils import *
import itertools

class LSH():
    def __init__(self, signature_mat:list, b:int, r:int):
        self.signature_mat = signature_mat
        self.b = b
        self.r = r
        assert b*r == len(signature_mat[0]) , "The product b*r should be equal to the number of rows in the signature matrix"
        self.similar_docs = set()
        self.hash_fn = hashFamily(32)

    def computeLSH(self) -> set:
        hash_in_docs = dict()
        for i in range(self.b):
            band = []
            hashed_columns = []
            for column in (self.signature_mat):
                start = i*self.r
                end = start + self.r 
                #print(i,column[start:end])
                band.append(column[start:end])
                #print(self.signature_mat[j][start:end])
            for c in band:
                #print(c)
                p = str(tuple(c)) #I can only hash immutable types -> from list to tuple 
                hashed_columns.append(self.hash_fn(p))
            #print(i,hashed_columns)
            for i,item in enumerate(hashed_columns):
                if item in hash_in_docs:
                    if i not in hash_in_docs[item]:
                        hash_in_docs[item].append(i)
                else:
                    hash_in_docs[item] = [i]

        for e in hash_in_docs.values():
            if len(e)>1: #I have near duplicates
                #since I can have more than two near duplicates for a band I need the combinations of the pairs 
                for subset in itertools.combinations(e,2):
                    self.similar_docs.add(tuple(subset))

        return self.similar_docs

    def __str__(self):
        return "Similar documents: %s"%(self.similar_docs)

    
