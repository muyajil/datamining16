import numpy as np

# articles
m = 0
A = np.array([])
ids = []
means = dict()
counts = dict()
last_c = 0
last_user = np.array([])
M = dict()
b = dict()

t = 1

def set_articles(articles):

    global A
    global ids
    global counts
    global M

    ids = articles.keys()
    A = np.zeros((len(ids),6))
    counts = {id: 0 for id in ids}
    M = {id: np.array([]) for id in ids}
    b = {id: np.array([]) for id in ids}
    i = 0
    for id in ids:
        A[i] = articles[id]
        i+=1

def update(reward):
    global counts
    global last_c
    global last_user
    global t

    # choice wasnt made
    if reward == -1:
        return

    M[last_c] = M[last_c] + np.outer(last_user, last_user)
    b[last_c] = b[last_c] + np.multiply(reward, last_user)
    counts[last_c]+=1
    t+=1

def recommend(time, user_features, choices):
    global M
    global b
    global last_c
    global last_user

    delta = 0.9999
    alpha = 1 + np.sqrt(np.log(2/delta)/2.0)
    z = user_features

    max_ucb = 0
    c = choices[0]
    for choice in choices:

	# new choice
	if counts[choice] == 0:
	    M[choice] = np.identity(len(user_features))
	    b[choice] = np.zeros(len(user_features))

        # LinUCB Algorithm
	w = np.linalg.solve(M[choice], b[choice])
	ucb = np.dot(w, z) + alpha * np.sqrt(np.dot(z, np.linalg.solve(M[choice], z)))
	if ucb > max_ucb:
	    max_ucb = ucb
	    c = choice

    last_user = z
    last_c = c
    return c
