from utils import *
import itertools

class LSH():
    """
    Implementation of the LSH algorithm
    """
    def __init__(self, signature_mat:list, b:int, r:int):
        self.signature_mat = signature_mat
        self.b = b #number of bands
        self.r = r #number of rows for each band
        assert b*r == len(signature_mat[0]) , "The product b*r should be equal to the number of rows in the signature matrix"
        self.similar_docs = set()
        self.hash_fn = hashFamily(100)

    def computeLSH(self) -> set:
        """
        Divide the signature matrix in bands and compute the hash for every column of every single band,
        if two column of the same band have the same hash, then the two docs are neighbours

        Returns:
            set: set of possible duplicates
        """
        #hash_in_docs = dict() #{hash:[list of columns with such hash]}
        #build the bands
        for i in range(self.b):
            hash_in_docs = dict() #{hash:[list of columns with such hash]}
            band = []
            hashed_columns = []
            #append band of each column
            for column in (self.signature_mat):
                start = i*self.r
                end = start + self.r 
                band.append(column[start:end])
            #compute hash for the columns of the band
            for c in band:
                p = str(tuple(c)) #I can only hash immutable types -> from list to tuple 
                hashed_columns.append(self.hash_fn(p))
            #build the buckets
            for i,item in enumerate(hashed_columns):
                if item in hash_in_docs:
                    if i not in hash_in_docs[item]:
                        hash_in_docs[item].append(i)
                else:
                    hash_in_docs[item] = [i]
            #take the pairs from the list of collisions 
            for e in hash_in_docs.values():
                if len(e)>1: #I have near duplicates
                    #since I can have more than two near duplicates for a band I need the combinations of the pairs 
                    for subset in itertools.combinations(e,2):
                        self.similar_docs.add(tuple(subset))

        return self.similar_docs

    def __str__(self):
        return "Similar documents: %s"%(self.similar_docs)

    
