import numpy as np
import random as rand

epochs = 1
alpha = 0.0001
t0 = 2000

m = 3000
d = 400
featutes = m

W = np.random.randn(d, m)
b = np.random.random_sample(size=m) * 2 * np.pi


def transform(X):
    # Make sure this function works for both 1D and 2D NumPy arrays.

    # str(X.shape) = (400,)
    # str(W.shape) = (400, m)
    # str(b.shape) = (m,)

    Z = np.cos(X.dot(W) + b) * np.sqrt(2.0/float(m))
    # str(temp.shape) = (m,)

    return Z

def learning_rate(t):
    # return 1.0/(np.sqrt(t))
    return 1.0/(alpha * (t + t0))

def mapper(key, value):
    # key: None
    # value: 5k lines, each (y | x0 | .. | x399)

    num_samples = len(value)

    # initialize
    w = np.random.randn(featutes)
    t = 0
    # decay rates for momentum estimates
    beta1 = 0.9
    beta2 = 0.999
    epsilon = 0.00000001
    # moment vectors
    mom  = 0
    v = 0

    for i in range(epochs):
        rand.shuffle(value)
        updates = 0

        for sample in value:
            
	    t+=1
	    sample = sample.split()
            y = int(sample[0])

	    x = transform(np.array(map(float, sample[1:])))

            if (np.dot(w, x) * y < 1):
		grad = y * x                
		mom = beta1 * mom + (1 - beta1) * grad
                v = beta2 * v + (1 - beta2) * (grad**2)		
		mhat = mom/(1-(beta1**t))
                vhat = v/(1-(beta2**t))		
		w += learning_rate(t) * mhat / (np.sqrt(vhat) + epsilon)	
		updates += 1

        if updates < 1000:
            break


    yield "weightvector", w  # This is how you yield a key, value pair


def reducer(key, values):
    # key: key from mapper used to aggregate
    # values: list of all value for that key
    # Note that we do *not* output a (key, value) pair here.
    w = np.zeros(featutes)
    for value in values:
        w += value
    yield w/len(values)





