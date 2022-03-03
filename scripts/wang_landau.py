import numpy as np
import itertools
from func_wang_landau import *
import time as time

def wang_landau(l,n_bins,wall_time=300,f_final=1):
    # Set timer
    start_time = time.time()
    
    # Initalize default values
    f = np.e 
    acc = 0.5
    check = 10000*l**2
    check_counter = 1

    # Initalize empty histogram
    E_min = min_E(l)
    E_max = max_E(l)
    hist = H(E_min,E_max,n_bins)

    # Initalize model 
    model = config(l)
    
    # Loop the algorithm
    while True:
        # Set a walltime to end the algortihm if it goes to long
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > wall_time:
            return hist, f

        # Check the flatness of the algortihm every X steps outlined by the
        # literature
        if check_counter % check == 0:
            if flatness(hist,acc):
        # End the algortihm if f gets small enough
                if f <= f_final:
                    return hist
        # Update f, reset hist, make a new inital config
                f = f**0.5
                hist = H(E_min,E_max,n_bins)
                model = config(l)
        
        # propose a move
        move = random_change(model)
        
        # Measure the energies for the moves
        E_1 = energy(model)
        E_2 = energy(move)
        


