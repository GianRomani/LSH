from utils import *
import heapq

class MinwiseHashing:

    def __init__(self, collection:set, n_of_hash:int):
        self.collection = collection #collection of set of shingles
        self.number_of_docs = len(self.collection)
        self.hash_fn = hashFamily(32)
        self.n_of_hash = n_of_hash
        self.ordered_shingles = []
        self.signature_matrix = [] #or numpy?

    def orderShingles(self):
        set_of_shingles = set()
        for doc in self.collection:
            for s in doc:
                set_of_shingles.add(s)
        #now order
        for i in set_of_shingles:
            heapq.heappush(self.ordered_shingles, i)
        self.len_ordered_shingles = len(self.ordered_shingles)

    def populate_signature_matrix(self):
        for i in range(self.len_ordered_shingles):
            for j,doc in enumerate(self.collection):
                if self.ordered_shingles[i] in self.collection[doc]: #I can not use collection[doc]
                    self.signature_matrix[i][j] == 1
                else:
                    self.signature_matrix[i][j] == 0


    def __str__(self) -> str:
        return "Signature Matrix: %s" %(self.signature_matrix)