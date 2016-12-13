import numpy as np

k = 7

def mapper(key, value):
    # key: None
    # value: one line of input file

    # value.shape = (10000, 250)
    # each value is a 250 dimensional feature vector

    # D^2 sampling (bicriteria approximation)
    # iteratively sample data points as new centers proportional
    # to squared distance to existing cluster centers
    np.random.shuffle(value)
    D = np.zeros(10000)
    B = np.zeros((k, 250))
    b = 1
    i = 0
    # TODO: i overflow
    while b < k
	# initialize first cluster, initialize distances
        if i==0:
	    B[0] = value[0]
	    for j in range(10000):
		D[j] = np.norm(value[j]-B[0])**2
            continue
            
	# sum of squared distances
	sums = 0
	for j in range(10000):
	    sums += (D[j]**2)

	# proportional sampling
        while ans==0:
            p = D[i]/sums
	    ans = np.random.binomial(1, p)
            i++

        # new center
	B[b] = value[i]
        b++

	# update distances
	for j in range(10000):
	    newD = np.norm(value[j]-B[b])**2
            if D[j] > newD:
		D[j] = newD
    #endwhile

    # Coreset using importance sampling
    

    # All mappers should output the same key
    yield "key", "value"  # this is how you yield a key, value pair


def reducer(key, values):
    # key: key from mapper used to aggregate
    # values: list of all value for that key
    # Note that we do *not* output a (key, value) pair here.

    # TODO: use coreset composition here

    # Reducer should output a 2D NumPy array containing 200 vectors representing the selected centers (each being 250 floats).
    yield np.random.randn(200, 250)
