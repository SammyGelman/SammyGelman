import numpy as np
import random

def ising_model(N=8,T=1.0,J=0):
    model = np.zeros((N,N))
    for i in range(L):
        for j in range(L):
            if random.random() >= 0.5:
                model[i,j] = 1
            else:
                model[i,j] = -1

