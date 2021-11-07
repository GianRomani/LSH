
from Shingles import *
class Neighbours:

    def __init__(self, threshold:float):
        self.threshold = threshold
        self.similar_docs = set()

    def Jaccard_sim(self, shingle1:Shingle, shingle2:Shingle) -> float:
        """Compute the Jaccard similarity between two set of hashed shingles -> |shingle1 ∩ shingle2|/|shingle1 ∪ shingle2|

        Args:
            shingle1 (Shingle): set of hashed shingles for the first document
            shingle2 (Shingle): set of hashed shingles for the second document

        Returns:
            float: jaccard similarity result
        """
        set1 = shingle1.shingle_set
        set2 = shingle2.shingle_set
        union = set1.union(set2)
        intersection = set1.intersection(set2)
        jaccard_sim = len(intersection) / len(union)
        return jaccard_sim

    def compare_docs(self, set_of_shingles:list)->set:
        """
        Given a collection of the sets of shingles for the documents, 
        compute the jaccard similarity for all the pairs and then filter using the threshold.

        Args:
            set_of_shingles (list): collection of sets of hashed shingles

        Returns:
            set: set of pairs that are similar enough
        """
        n_of_doc = len(set_of_shingles)
        for s1 in range(n_of_doc):
            #Compare with the following documents
            for s2 in range(s1+1, n_of_doc):
                j_sim = self.Jaccard_sim(set_of_shingles[s1],set_of_shingles[s2])
                if(j_sim>=self.threshold):
                    doc1 = set_of_shingles[s1].docId
                    doc2 = set_of_shingles[s2].docId
                    self.similar_docs.add((doc1,doc2))
        return self.similar_docs

