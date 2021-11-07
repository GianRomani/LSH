from MinwiseHashing import MinwiseHashing
from Shingles import *
from LSH import *
import csv 
from utils import *
import time


def Jaccard_sim(shingle1:Shingle, shingle2:Shingle) -> float:
    """[summary]

    Args:
        shingle1 (Shingle): [description]
        shingle2 (Shingle): [description]

    Returns:
        float: [description]
    """
    set1 = shingle1.shingle_set
    set2 = shingle2.shingle_set
    union = set1.union(set2)
    intersection = set1.intersection(set2)
    jaccard_sim = len(intersection) / len(union)
    return jaccard_sim

def compare_docs(set_of_shingles:list, threshold: float)->dict:
    similar_docs = set()
    n_of_doc = len(set_of_shingles)
    for s1 in range(n_of_doc):
        for s2 in range(s1+1, n_of_doc):
            j_sim = Jaccard_sim(set_of_shingles[s1],set_of_shingles[s2])
            #print(s1,s2,j_sim)
            if(j_sim>=threshold):
                doc1 = set_of_shingles[s1].docId
                doc2 = set_of_shingles[s2].docId
                similar_docs.add((doc1,doc2))
    return similar_docs

print("Write path to the tsv file containing the jobs' announcements:")
#path = input()
#path = '/home/gianfree/Desktop/Data Mining/HW2/LSH/batch_aa.tsv'
#path = '/home/gianfree/Desktop/Data Mining/HW2/LSH/splits/newab.tsv'
path = '/home/gianfree/Desktop/Data Mining/HW2/LSH/jobs.tsv'
set_of_shingles = []

with open(path, 'r') as f:
    read_tsv = csv.reader(f, delimiter="\t")
    next(read_tsv) #just the head
    for i,row in enumerate(read_tsv):
        try:
            description = preprocess(row[1])
            shingle = Shingle(10, i)
            shingle.createShingles(description)
            set_of_shingles.append(shingle)
        except Exception as e:
            print(e)
            continue
    print("Shingles are ready!") 
                  
f.close()

print("Number of documents: {}".format(len(set_of_shingles)))

print("Populating the signature matrix...")
start = time.time()
minhashing = MinwiseHashing(set_of_shingles,100)
minhashing.orderShingles()
minhashing.signatureMatrix()
end = time.time()
print("...Done!")
print("Time spent for MinHashing: {}".format(end-start))

print("LSH is working...")
start = time.time()
lsh = LSH(minhashing.signature_matrix,20,5)
similar_docs_lsh = lsh.computeLSH()
end = time.time()
print("...Done!")
print("Time spent for LSH algorithm: {}".format(end-start))

#print(lsh)

print("Finding near-duplicates among all the announcements using Jaccard similarity of shingles...")
start = time.time()
near_duplicates = compare_docs(set_of_shingles, 0.80)
end = time.time()
print("...Done!")
print("Time spent for computing Jaccard similarity among all the documents: {}".format(end-start))
#print("Nearest documents: {}".format(near_duplicates))

print("LSH finds {} duplicates, the comparison of the shingles {}".format(len(similar_docs_lsh), len(near_duplicates)))

intersection = similar_docs_lsh.intersection(near_duplicates)
#print("Intersection of the results of the two methods is: {}".format(intersection))
print("The intersection has {} elements".format(len(intersection)))

#filter results obtained from LSH and plot intersection for different values of r and b
#Compute False positive and false negative