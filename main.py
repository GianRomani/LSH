from MinwiseHashing import MinwiseHashing
from Shingles import *
from LSH import *
import csv 
from utils import *
import time


#print("Write path to the tsv file containing the jobs' announcements:")
#path = input()
path = '/home/gianfree/Desktop/Data Mining/HW2/LSH/batch_aa.tsv'
#path = '/home/gianfree/Desktop/Data Mining/HW2/LSH/jobs.tsv'
set_of_shingles = []

print("Reading the file and extracting the shingles...")
with open(path, 'r') as f:
    read_tsv = csv.reader(f, delimiter="\t")
    next(read_tsv) #just the head
    for i,row in enumerate(read_tsv):
        try:
            #title = preprocess(text[0])
            description = preprocess(row[1])
            #print(description)
            #location = text[2]
            shingle = Shingle(10, i)
            shingle.createShingles(description)
            #print("DocId: {}'s shingles: {}".format(i,shingle))
            set_of_shingles.append(shingle)
            #print(shingle)
        except Exception as e:
            print(e)
            break
    print("Shingles are ready!") 
                  
f.close()
set1 = set_of_shingles[0]
set2 = set_of_shingles[1]
j = Jaccard(set1,set2)
print(j)
print("Populating the signature matrix...")
start = time.time()
minhashing = MinwiseHashing(set_of_shingles,100)
minhashing.orderShingles()
minhashing.signatureMatrix()
end = time.time()
print("Minhashing completed!")
print("Time spent for MinHashing: {}".format(end-start))

#print(minhashing)