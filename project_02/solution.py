import numpy as np
import random as rand

epochs = 1
alpha = 0.0001
t0 = 1000


m = 600
d = 400

W = np.random.randn(d, m)
b = np.random.random_sample(size=m) * 2 * np.pi


def transform(X):
    # Make sure this function works for both 1D and 2D NumPy arrays.

    # str(X.shape) = (400,)
    # str(W.shape) = (400, 500)
    # str(b.shape) = (500,)

    Z = np.cos(X.dot(W) + b) * np.sqrt(2.0/float(m))
    # str(temp.shape) = (500,)

    return Z

def learning_rate(t):
    # return 1.0/(np.sqrt(t))
    return 1.0/(alpha * (t + t0))

def mapper(key, value):
    # key: None
    # value: 5k lines, each (y | x0 | .. | x399)

    num_samples = len(value)

    # initialize weight vector
    w = np.random.randn(m)
    t = 0
    for i in range(epochs):
        rand.shuffle(value)
        updates = 0
        for sample in value:
            t+=1
            sample = sample.split()
            y = int(sample[0])
            x = transform(np.array(map(float, sample[1:])))

            if (np.dot(w, x) * y < 1):
                # classified wrong
                # take a step in the negative gradient direction
                updates += 1
                w += learning_rate(t) * y * x
                w *= min(1, 1/(alpha * np.linalg.norm(w,2)))

        if updates < 1000:
            break


    yield "weightvector", w  # This is how you yield a key, value pair


def reducer(key, values):
    # key: key from mapper used to aggregate
    # values: list of all value for that key
    # Note that we do *not* output a (key, value) pair here.
    w = np.zeros(m)
    for value in values:
        w += value
    yield w/len(values)





