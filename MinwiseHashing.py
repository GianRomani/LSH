from utils import *
import heapq
import sys

class MinwiseHashing:
    """
    Build the signature matrix
    """
    def __init__(self, collection: list, n_of_hash:int=100):
        self.collection = collection #collection of set of shingles
        self.number_of_docs = len(self.collection)
        self.ordered_shingles = [] 
        self.hash_family = [] #we want to use several hash functions, one for each row of the signature matrix
        self.n_of_hash = n_of_hash
        #populate list of hash functions
        for i in range(self.n_of_hash):
            j=100+i
            self.hash_family.append(hashFamily(j))

    def numberOfShingles(self):
        self.set_of_shingles = set()
        #take all the possible shingles
        for doc in self.collection:
            for s in doc.shingle_set:
                self.set_of_shingles.add(s)

        self.number_of_shingles = len(self.set_of_shingles)
        print("Number of distinct shingles: {}".format(self.number_of_shingles))

    def orderedShingles(self) -> list:
        for i in self.set_of_shingles:
             heapq.heappush(self.ordered_shingles, i)
        return self.ordered_shingles

    def signatureMatrix(self):
        """
        Build the signature matrix
        """
        self.signature_matrix = []
        for shingle_doc in self.collection: #for each document...
            signature = []
            hash_integer = 0 

            for h in self.hash_family: #for each hash function, i.e. for each row of the signature matrix
                minHashSignature = 2**64 #big number
                for s in shingle_doc.shingle_set:
                    #Compute hash and the smallest index for the permuted row containing a shingle
                    hashSignature = int.from_bytes(h(str(s)), sys.byteorder) %self.number_of_shingles
                    if hashSignature < minHashSignature:
                        minHashSignature = hashSignature
                #append signature oto the doc column
                signature.append(minHashSignature)
            #append the document column to the matrix
            self.signature_matrix.append(signature)


    def __str__(self) -> str:
        return "Signature Matrix: %s" %(self.signature_matrix)