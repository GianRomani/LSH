from MinwiseHashing import MinwiseHashing
from Shingles import *
from LSH import *
from NearestNeighbours import *
import csv 
from utils import *
import time
import os

def main():
    try:
        path = os.getcwd() +"/docs/jobs.tsv"
    except Exception as e: #insert manually the path
        print("Type the path to the folder containing the files:")
        path = input()
        path = path + "/jobs.tsv"

    set_of_shingles = []
    #Time to the get the shingles from the documents
    with open(path, 'r') as f:
        read_tsv = csv.reader(f, delimiter="\t")
        next(read_tsv) #just the head
        for i,row in enumerate(read_tsv):
            #get the shingles from the description field of each document
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
    #Build a signture matrix of 100 rows
    minhashing = MinwiseHashing(set_of_shingles,100)
    minhashing.numberOfShingles()
    minhashing.signatureMatrix()
    end = time.time()
    print("...Done!")
    print("Time spent for MinHashing: {}".format(end-start))
    
    #Use LSH with 20 bands of 5 rows each
    print("LSH is working...")
    start = time.time()
    lsh = LSH(minhashing.signature_matrix,20,5)
    similar_docs_lsh = lsh.computeLSH()
    end = time.time()
    print("...Done!")
    print("Time spent for LSH algorithm: {}".format(end-start))

    #Find near-duplicates using Jaccard on hashed shingles (threshold of 80%)
    print("Finding near-duplicates among all the announcements using Jaccard similarity of shingles...")
    start = time.time()
    threshold = 0.80
    duplicates = Neighbours(threshold)
    duplicates.compare_docs(set_of_shingles)
    near_duplicates = duplicates.similar_docs
    end = time.time()
    print("...Done!")
    print("Time spent for computing Jaccard similarity among all the documents: {}".format(end-start))

    print("LSH finds {} duplicates, the comparison of the shingles {}".format(len(similar_docs_lsh), len(near_duplicates)))

    #Compute intersection of the two methods
    intersection = similar_docs_lsh.intersection(near_duplicates)
    print("The intersection has {} elements".format(len(intersection)))

    #Near-duplicates
    true_positives = len(near_duplicates)
    #all possible pairs n!/(2!(n-2)!) if n is the number of documents
    possible_pairs = len(set_of_shingles)*(len(set_of_shingles)-1)/2
    true_negatives = possible_pairs - true_positives
    #Compute false positive and false negative
    false_negatives = len(near_duplicates) - len(intersection)
    false_positives = len(similar_docs_lsh) - len(intersection)
    #FP = FP/(FP+TN), FN = FN/(FN+TP)
    print("False positive rate: {}\nFalse negative rate: {}".format(false_positives/(false_positives+true_negatives), false_negatives/(false_negatives+true_positives)))


if __name__ == "__main__":
    main()