from random import seed, randint

MAX_SHINGLE_ID = 8193
'''
To start we needed to find out how we need to build our solution in the MapReduce setting.
We know we need to have a AND/OR construction to get the desired S curve effect.
Therefore we applied the technique from the lecture where we banded the matrix. 
The condition that a combination of two movies is a candidate for a near duplicate is
that it matches for a hash table across at least one band. Therefore it makes sense
that we emit the band id together with the hash table as a key.
The reducer then gets per band all movies in a list that are candidate pairs, and must
only check them pairwise and emit the ones that truly have a estimated Jaccard similarity of
0.85 and more.

Find parameters:

Plot function and find out for which r and b we have f(0.85) close to 0.5
We want to include false positives and exclude false negatives since then "only" have more work
First we had 15 and 10 (f(0.854) = 0.5), but then we increased b such that we have FN = 0

After trying to plot and tune to find the optimal parameters we tried finding them programmatically
to yield the parameters that have zero(1-(1-x^r_and)^b_or - 0.5) as close as possible to 0.85
by trying a lot of different combinations that match the criteria
We got 0.8499 for r_and = 25 and b_or = 40 -> this takes really long to compute
Therefore we found the top 10 best estimations and tried one with smaller params


Top 10 Estimates

1:      25      40      0.849963587962		too long
2:      16      9       0.849909922397		0.875
3:      24      34      0.849908093023		too long
4:      23      29      0.84971177389		too long
5:      19      15      0.849565296109		0.925
6:      21      21      0.849409416841		too long
7:      22      24      0.850635569477		too long
8:      25      39      0.850817253854		too long
9:      22      25      0.849080827864		too long
10:     24      33      0.85095501451		too long

So that was not successful, everything takes waaaay too long.
Therefore we should limit the number of hash functions by a smaller number.
It seems that after exceeding 300 the computation takes too long
Therefore we tried the best estimate under 300 hash functions:

Top 10 Estimates using under 300 hash functions:

1:      16      9       0.849909922397		TP=49	FP=13	FN=1	Precision: 0.790	Recall: 0.980	F1 score: 0.875
2:      19      15      0.849565296109		TP=50	FP=4	FN=0	Precision: 0.926	Recall: 1.000	F1 score: 0.961538461538
3:      18      13      0.848458997918		TP=49	FP=8	FN=1	Precision: 0.860	Recall: 0.980	F1 score: 0.915887850467
4:      17      11      0.848355211318		TP=50	FP=12	FN=0	Precision: 0.806	Recall: 1.000	F1 score: 0.892857142857
5:      18      12      0.852136134534		TP=49	FP=7	FN=1	Precision: 0.875	Recall: 0.980	F1 score: 0.924528301887
6:      19      14      0.852582380384		TP=50	FP=3	FN=0	Precision: 0.943	Recall: 1.000	F1 score: 0.970873786408
7:      15      8       0.847104773562		TP=48	FP=14	FN=2	Precision: 0.774	Recall: 0.960	F1 score: 0.857142857143
8:      17      10      0.852968501975		TP=50	FP=13	FN=0	Precision: 0.794	Recall: 1.000	F1 score: 0.884955752212
9:      14      6       0.853637648804		TP=49	FP=14	FN=1	Precision: 0.778	Recall: 0.980	F1 score: 0.867256637168
10:     11      4       0.846107318111		TP=49	FP=14	FN=1	Precision: 0.778	Recall: 0.980	F1 score: 0.867256637168

Important is that we have FP=50 and FN=0, this tells us we have not missed any duplicate just because we chose params wrong

So the next step is to find out how much we can increase the number of hash functions, without taking too long to compute.

Top 10 Estimates using 300-350 hash functions:

1:      300     1       0.997692176527
2:      301     1       0.99769983489
3:      302     1       0.997707442593
4:      303     1       0.997715000139
5:      304     1       0.99772250802
6:      305     1       0.997729966725
7:      306     1       0.997737376735
8:      307     1       0.997744738526
9:      308     1       0.997752052568
10:     309     1       0.997759319322

Ok these are very bad, lets try to widen the scope a bit. After widening the search space to 300-1024 we still got the same results as above.
From that we that we get the best results if we use under 300 hash functions

So now we have our best estimate using 19 and 14 for our parameters, there is still a discrepancy between the local performance and the one
on the server. But without looking at the leaderboard this is our best solution on the local test set, therefore this solution should be
the one that performs best in terms of generalization.
'''

r_and = 19
b_or = 14
num_hashes = r_and*b_or

def mapper(key, value):

	# since each mapper will randomly choose params of hash functions, we want them to be the same for all mappers
	# Here we also tried different seeds just for fun. 6 achieved 100% on the local test set.
	seed(6)

	words = value.split()
	vid_id = int(words[0].split('_')[1])

	# features contains all rows which are 1 for the current coloumn in the "shingle matrix"
	features = map(int, words[1:])
	# sort by shingle_id
	features.sort()

	# initialize random hash functions
	a = []
	b = []
	for i in range(num_hashes):
		a.append(randint(1,9999))
		b.append(randint(0,9999))

	# Compute coloumn of signature matrix (value for each hash function)
	signature_col = [MAX_SHINGLE_ID]*(num_hashes)
	for feature in features:
		for i in range(num_hashes):
			res = (a[i]*feature+b[i])%MAX_SHINGLE_ID
			signature_col[i] = min(res, signature_col[i])

	# We want to aggregate all videos that match across one band
	# Therefore we use the hashes from the band as the key together with the id of the band
	# As the value we yield the video id and the signature coloumn
	# We need the signature coloumn to compute the approximated jaccard similarity
	for b in range(b_or):
		hashes = signature_col[b_or*r_and:b_or*r_and+r_and]
		yield (str(b) + ',' + str(hashes)), (vid_id, signature_col)

def similarity(sig1, sig2):
	# Compute estimated Jaccard similarity
	num_matches = 0
	for i in range(num_hashes):
		if sig1[i] == sig2[i]:
			num_matches += 1
	return num_matches/float(num_hashes)

def reducer(key, values):
    # Here we receive per key, all videos that match across the same band
    # Each value is a tuple containing video id and signature_col
    # first we need to sort the values in ascending order 
    # the sorting saves time, since we only need to look at pairs i,j with i < j
    values.sort(key=(lambda x: x[0]))

    # Now we can compare each video with all videos that have a bigger id
    for i in range(len(values)):
    	for video in values[i+1:]:
    		if(similarity(video[1], values[i][1]) >= 0.85):
    			yield values[i][0], video[0] 
