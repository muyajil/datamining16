import numpy as np
import math

# number of bicriteria points in the D2 sampling
k = 200

# number of representatives each mapper produces
kk = 200

# number of representatives to produce
kr = 200

# number of data points for each mapper
N = 10000

# number of mappers
nm = 10

def mapper(key, value):

    ##############################################
    # 1. D^2 sampling (bicriteria approximation) #
    ##############################################

    np.random.shuffle(value)
    B = np.zeros((k, 250))	# B = The Bicriteria points
    B[0] = value[0]		# First point is sampled uniformly at random
    D = np.zeros(N)		# D = Distance to closest bicriteria point (so far)
    Mins = [0]*N		# Mins = closest bicriteria point (so far)

    # For each point, initialize its distance to the distance to the first
    # bicriteria point
    for i in range(N):
	D[i] = np.linalg.norm(value[i]-B[0])

    # In each step, sample a data point as new center proportional to
    # squared distance to existing cluster centers
    for b in range(k):

	# proportional sampling
        prob = np.divide(np.square(D), np.sum(np.square(D)))
        newCenter = np.random.choice(range(N), p=prob)
	B[b] = value[newCenter]

        # update distances
	for i in range(N):
	    newD = np.linalg.norm(value[i]-B[b])
            if D[i] > newD:
		D[i] = newD
		Mins[i] = b


    ##############################################
    # 2. Coreset using importance sampling       #
    ##############################################

    alpha = math.log(k,2) + 1	    	   # see slides
    avgs = np.sum(np.square(D))/float(N)   # average distance to closest bic. point
    ssumB = np.zeros(k)			   # sum of squared distances for each "cluster"
    Bi = np.zeros(k)			   # number of points for each cluster
    upperBound = np.zeros(N)		   # upper bound on sensitivity for each point

    # Compute Bi and ssumB
    for i in range(N):
	Bi[Mins[i]] += 1		   # simply count the points in each cluster
	ssumB[Mins[i]] += D[i]**2	   # add up the squared distances

    # Compute upper bound on sensitivity for each point
    for i in range(N):
	upperBound[i] = (alpha * D[i]**2) / avgs
	upperBound[i] += (2 * alpha * ssumB[Mins[i]]) / (Bi[Mins[i]] * avgs)
	upperBound[i] += float(4*N) / float(Bi[Mins[i]])

    # Sample proportional to upper bound of sensitivity
    q = np.divide(upperBound, np.sum(upperBound))
    representatives_num = np.random.choice(range(N), size=kk, p=q, replace=False)

    representatives = np.zeros((kk, 250))
    for i in range(kk):
	representatives[i] = value[representatives_num[i]]

    print 'mapper done'

    # All mappers should output the same key
    yield "key", representatives


def reducer(key, values):
    # key: key from mapper used to aggregate
    # values: list of all value for that key
    # Note that we do *not* output a (key, value) pair here.

    # 3rd approach: d2 sampling + k-means
    ##############################################
    # 1. D^2 sampling (bicriteria approximation) #
    ##############################################
    np.random.shuffle(values)
    B = np.zeros((kr, 250))
    B[0] = values[0]
    NN = kk * nm		# number of points for the reducer
    D = np.zeros(NN)
    Mins = [0]*(NN)
    for i in range(NN):
	D[i] = np.linalg.norm(values[i]-B[0])**2
    for b in range(kr):
        prob = np.divide(np.square(D), np.sum(np.square(D)))
        newCenter = np.random.choice(range(NN), p=prob)
	B[b] = values[newCenter]
	for i in range(NN):
	    newD = np.linalg.norm(values[i]-B[b])**2
            if D[i] > newD:
		D[i] = newD
		Mins[i] = b
    ##############################################
    # 2. standard K-means                        #
    ##############################################
    # B = centers
    # Mins = nearest center for each point
    steps = 0
    while True:

        # 1. Assignment step
	for i in range(NN):
   	    mindist = np.linalg.norm(values[i]-B[0])
	    Mins[i] = 0
	    for b in range(kr):
		distance = np.linalg.norm(values[i]-B[b])
                if mindist > distance:
		    Mins[i] = b
		    mindist = distance

        # 2. Update step
	oldB = B
        B = np.zeros((kr, 250))
        ClusterCount = np.zeros(kr)
        for i in range(NN):
            B[Mins[i]] += values[i]
	    ClusterCount[Mins[i]] += 1
	for b in range(kr):
	    B[b] = np.divide(B[b], ClusterCount[b])

	# 3. Convergence
        steps+=1
        print 'kmean step'
	if np.array_equal(oldB, B) or steps == 30:
	    break

    yield B

    # 2nd approach: merge AND compression

    # 1st approach: use coreset composition here
    #yield values







