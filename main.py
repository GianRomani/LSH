from Shingles import *
import csv 
from utils import *
import heapq

def sort_shingles(set_of_shingles: set)->list:
    sorted = []

    return sorted

#print("Write path to the tsv file containing the jobs' announcements:")
#path = input()
path = '/home/gianfree/Desktop/Data Mining/HW2/jobs.tsv'
set_of_shingles = set()

with open(path, 'r') as f:
    read_tsv = csv.reader(f, delimiter="\t")
    next(read_tsv) #just the head
    for i,row in enumerate(read_tsv):
        try:
            text = next(read_tsv)
            #title = preprocess(text[0])
            description = preprocess(text[1])
            #print(type(description))
            #location = text[2]
            shingle = Shingle(10, i)
            shingle.createShingles(description)
            set_of_shingles.add(shingle)
        except Exception as e:
            print(e)
            break
    print("Shingles are ready!")               
f.close()