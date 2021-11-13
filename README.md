# LSH - Implementation of Locality Sensitive Hashing algorithm for jobs announcements in Kijiji website

This project was made for a Data Mining course (winter 2021).
To run the program use: python main.py.
The main just calls the functions defined in the other files, keeps track of the time needed to use the two approaches for nearest-neighbours and print some statistics (false positives, number of duplicates etc).
The problem of finding duplicates is tackled into three steps: making of shingles, building a signature matrix and applying LSH to this matrix.

To obtain the shingles, the program opens the file with the announcements, takes the description and preprocesses it. In utils.py there is the code for the preprocessing and the function for implementing a family of hash functions (given by the teacher). I implemented functions to clean the textual data from html elements, accented chars, stopwords, punctuation and numbers and there are also two functions devoted to apply stemming and lemmatization to the tokens. By calling the function preprocess() I can decide which actions, from the ones listed above, perform on the strings. At the end I decided to use all the previous functions, except for lemmatizer() and remove_accented_chars() because the stemmer does a better job than the lemmatizer and it makes little sense to use both accented_chars() and the stemmer, but I kept them in the code anyway.
Shingle.py contains the code relative to the creation and hashing of shingles, given a certain document. The dimension of the shingles is set to 10 characters.

The minhashing step is performed in the MinHashing class (located into the MinHashing.py file). When a MinHashing object is instantiated, a list of <i>n_of_hash</i> hash functions is created (the number of them depends on how many rows we want in our signature matrix, in my case I fixed it to 100, which is generally the recommended value). We can finally build the signature matrix using the signatureMatrix() method, which gets the shingles for each document and then for every hash function from the <i>n_of_hash</i> available ones it saves in the signature matrix the minimum value among the hashed shingles. I decided to compute for each hashed shingle from the previous step the following module operation: hashSignature % number_of_shingles, to obtain smaller values (so the computation of a signature matrix of 100 rows is 3-4 seconds faster) and to simulate the computation of an index given by a random permutation of the row (so we are saving in the signature matrix the smaller index, i.e. the index of the first row inhabited by a shingle).

When we have the signature matrix, we can pass it to the LSH algorithm to find duplicates among the documents. In LSH.py there is the class assigned to this task, which has the computeLSH() method that divides the signature matrix into <i>b</i> bands of <i>r</i> rows and for each band it computes the hashes of the sections of columns that are then stored into the dictionary hash_in_docs that has as key the hash value and as value a list of columns that have the same hash for that band. At this point we just need to get the pairs from the list of collisions (done by using itertools.combination() method) and move to the next band.

After the end of the LSH algorithm, to check if the pairs returned are good enough, it is time to find the nearest-duplicates using just the Jaccard similarity on the hashed shingles of the documents. To do so there is the class Neighbours (NearestNeighbours.py) that has two methods, one that computes the Jaccard similarity on two sets of shingles, and a second that just iterates over every possible pair of documents and calls the first method.

Lastly I compute the intersection over the sets returned by LSH and Neighbours, the false positive rate and the false negative rate. In the images in the following pages I reported the results I obtained in some tests I did for different values for the number of bands. We can notice how much LSH is faster than a brute force comparison of the shingles (4-23 vs 136-137 seconds). Since we want to find as much duplicates as we can, I think that I would exclude the first choice of parameters (10 bands of 10 rows), even if the false rate negative is very low, and from the other three I would choose the version with 20 bands because it is the faster (LSH has to compute hashes for less bands) and also it has the lowest false positive rate. The number of false positive can be decreased by filtering the results of LSH by comparing the shingles. The high number of duplicates is given by the fact that most of the documents, 1900 more or less, have the same description (even if they have different titles, timestamp and location), this description is\textit{ "Clicca sul link sottostante "sito web" per inviarci la tua candidatura"}. To avoid this fact it could be useful to take also other fields from the jobs.tsv file (the title for example).

10 bands of 10 rows each:
![10_10](https://user-images.githubusercontent.com/49344669/141646641-8cce5f87-b008-4604-aec4-b5c8d42b2615.jpeg)

20 bands of 5 rows each:
![20_5](https://user-images.githubusercontent.com/49344669/141646643-7481b863-97ec-46c9-a94c-8fb3b70bc969.jpeg)

25 bands of 4 rows each:
![25_4](https://user-images.githubusercontent.com/49344669/141646644-9a415545-36b7-4f8a-aca0-80a475128f41.jpeg)

50 bands of 2 rows each:
![50_2](https://user-images.githubusercontent.com/49344669/141646645-cc3b0545-dfbb-4cf2-8bc7-dc0988aef4b6.jpeg)
