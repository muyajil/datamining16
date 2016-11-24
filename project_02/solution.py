import numpy as np
import random as rand

def transform(X):
    # Make sure this function works for both 1D and 2D NumPy arrays.
    return X

def learning_rate(t):
    return 1/np.sqrt(t)

def mapper(key, value):
    # key: None
    # value: 5k lines, each (y | x0 | .. | x399)

    num_samples = len(value)

    # initialize weight vector
    w = np.random.randn(400)
    for i in range(1):
        updates = 0
        t = 0
        for sample in value:
            t+=1
            sample = sample.split()
            y = int(sample[0])
            x = np.array(map(float, transform(sample[1:])))

            if (np.dot(w, x) * y < 1):
                # classified wrong
                # take a step in the negative gradient direction
                updates += 1
                w += learning_rate(t) * y * x
                w *= min(1, 1/np.linalg.norm(w,2))
        if updates < 1000:
            break


    yield "weightvector", w  # This is how you yield a key, value pair


def reducer(key, values):
    # key: key from mapper used to aggregate
    # values: list of all value for that key
    # Note that we do *not* output a (key, value) pair here.
    w = np.zeros(400)
    for value in values:
        w += value
    yield w/len(values)
