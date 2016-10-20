from random import seed, randint

MAX_SHINGLE_ID = 8193

# Plot function and find out for which r and b we have f(0.85) close to 0.5
# We want to include false positives and exclude false negatives since then "only" more work
# First we had 15 and 10 (f(0.854) = 0.5), but then we increased b such that we have FN = 0

# After trying to plot and tune to find the optimal parameters we tried finding them programmatically
# to yield the parameters that have root(1-(1-x^17)^10 - 0.5) as close as possible to 0.85
# by trying a lot of different combinations that match the criteria
# We got 0.8499 for r_and = 25 and b_or = 40 -> this takes really long to compute
# Therefore we found the top 10 best estimations and tried one with smaller params
'''
Top 10 Estimates

1:      25      40      0.849963587962
2:      16      9       0.849909922397
3:      24      34      0.849908093023
4:      23      29      0.84971177389
5:      19      15      0.849565296109
6:      21      21      0.849409416841
7:      22      24      0.850635569477
8:      25      39      0.850817253854
9:      22      25      0.849080827864
'''


# Best score so far: 0.95/0.90, 15/15
r_and = 25 
b_or = 40 # 0 false negatives for 15
num_hashes = r_and*b_or

def mapper(key, value):

	# since each mapper will randomly choose params of hash functions, we want them to be the same for all mappers
	# Here we also tried different seeds
	seed(4)

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
