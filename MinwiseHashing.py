from utils import *
import heapq
import sys

class MinwiseHashing:

    def __init__(self, collection: list, n_of_hash:int=100):
        self.collection = collection #collection of set of shingles
        self.number_of_docs = len(self.collection)
        self.ordered_shingles = []
        self.hash_family = []
        self.n_of_hash = n_of_hash
        #populate list of hash functions
        for i in range(self.n_of_hash):
            j=100+i
            self.hash_family.append(hashFamily(j))

    def orderShingles(self):
        set_of_shingles = set()
        for doc in self.collection:
            for s in doc.shingle_set:
                set_of_shingles.add(s)
        #now order
        for i in set_of_shingles:
            heapq.heappush(self.ordered_shingles, i)
        self.len_ordered_shingles = len(self.ordered_shingles)
        print("Number of distinct shingles: {}".format(self.len_ordered_shingles))

    def signatureMatrix(self) -> list:
        self.signature_matrix = []
        for shingle_doc in self.collection:
            signature = []
            hash_integer = 0 

            for h in self.hash_family: 
                minHashSignature = 2**64
                #print(len(shingle_doc.shingle_set))
                for s in shingle_doc.shingle_set:
                    hashSignature = int.from_bytes(h(str(s)), sys.byteorder) %self.len_ordered_shingles
                    #print("{}, {}".format(hashSignature,minHashSignature))
                    if hashSignature < minHashSignature:
                        #print(hashSignature)
                        minHashSignature = hashSignature

                signature.append(minHashSignature)
            self.signature_matrix.append(signature)


    def __str__(self) -> str:
        return "Signature Matrix: %s" %(self.signature_matrix)