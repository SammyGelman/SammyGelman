import numpy as np
import itertools

def config(l):
    # randomly configure the model with dimensions lxl
    return np.random.randint(2,size=(l,l))*2 - 1

def random_index(config):
    # Generate random index on the model to flip
    ind_1 = np.random.randint(0,len(config))
    ind_2 = np.random.randint(0,len(config))
    return (ind_1,ind_2)

def random_flip():
    # Chose a spin to flip to randomly
    return np.random.randint(2)*2 - 1

def ising_hamiltonian(grid,J=1):
    # returns the energy of a given configuration 
    l = len(grid)
    E = 0
    for i, j in itertools.product(range(l),range(l)):
        S = grid[i,j]
        neighbor_interaction = grid[(i+1)%l, j] + grid[i,(j+1)%l] + grid[(i-1)%l, j] + grid[i,(j-1)%l]
        E += -neighbor_interactioni*J*S
    return E/2

def wang_landau(l,n_steps,f):
    g = 1
    model = gen_grid(l)
    for i in n_steps:
        index = random_index(model)

