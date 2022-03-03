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

def energy(grid,J=1):
    # returns the energy of a given configuration 
    l = len(grid)
    E = 0
    for i, j in itertools.product(range(l),range(l)):
        S = grid[i,j]
        neighbor_interaction = grid[(i+1)%l, j] + grid[i,(j+1)%l] + grid[(i-1)%l, j] + grid[i,(j-1)%l]
        E += -neighbor_interaction*J*S
    return E/2

def random_change(config):
    new_config = config.copy()
    new_config[random_index(new_config)] *= -1 
    return new_config

def prob_flip(E_1,E_2):
    return min(g(E_1)/g(E_2),1)

#function to find max and min energies of model givin length l
def min_E(l):
    return energy(np.ones((l,l)))

def max_E(l):
    model = np.ones((l,l))
    alternator = 0
    row_alternator = 0 
    if l % 2 == 1:
        for i in range(l):
            for j in range(l):
                if alternator % 2 == 0:
                    model[i,j] -= 2
                alternator += 1
    else:
        for i in range(l):
            for j in range(l):
                if alternator % l == 0:
                    row_alternator +=1
                if (alternator + row_alternator) % 2 == 0:
                    model[i,j] -= 2
                alternator += 1
    return energy(model)

#function to make empty histogram with n bins between min and max energies
def H(E_min, E_max, n_bins):
    hist = {}
    E_range = np.linspace(E_min, E_max, n_bins)
    for E in E_range:
        hist[E] = 0
    return hist

def indexer(x):
    return int(np.floor(x/2))

def find_bin(hist,E):
    # Get list of keys
    key_list = list(hist.keys())
    # Get init value for the index of search algorithm
    index = indexer(len(hist))
    # init value for history of algorithm
    history = 0
    # init value history of the history which will end the algorithm
    breaker = 0
    # init value for step size
    step = 0
    
    #count moves
    i = 0

    while breaker != index:
        if E > key_list[index]:
            breaker = history
            step = indexer(np.abs(index - history))
            if step == 0:
                step = 1
            history = index
            index += step

        elif E < key_list[index]:
            breaker = history
            step = indexer(np.abs(index - history))
            if step == 0:
                step = 1
            history = index
            index -= step
        
        else:
            return E, index
    return history

def update_hist(hist, index):
    key_list = list(hist.keys())
    hist[key_list[index]] += 1
    return hist

def g(hist,index,f):
    key_list = list(hist.keys())
    val = hist[key_list[index]]*f    
    if val == 0:
        return 1
    else:
        return val

# Check how flat a histogram is
def flatness(hist,acc):
# calculate the avg of all values of the histogram
    avg = sum(hist.values())/len(dist) 
# check that H(E) for all is no less than acc % from mean value
    for val in hist.values():
        if val < avg*acc:
            return False
    return True

# Catch lost samples

