#!/usr/bin/env python 

import numpy as np
import itertools
from func_wang_landau import *
import time as time
import random
import matplotlib.pyplot as plt

def wang_landau(l,n_bins,wall_time=3000,f_final=1):
    plt.ion()
    # Set timer
    start_time = time.time()

    # Initalize default values
    f = np.e
    acc = 0.5
    check = 100*l**2
    check_counter = 1

    # Initalize empty histogram
    E_min = min_E(l)
    E_max = max_E(l)
    hist = H(E_min,E_max,n_bins)
    print(hist)

    # Initalize model
    model = config(l)

    # Loop the algorithm
    while time.time() - start_time < wall_time:
        # Check the flatness of the algortihm every X steps outlined by the
        # literature
        if check_counter % check == 0:
            print('Checking...')
            vals = list(hist.values())
            log_val = []
            for val in vals:
                if val != 0:
                    log_val.append(np.log(val))
                else: 
                    log_val.append(val)
            # plt.bar(list(hist.keys()), hist.values())
            plt.bar(list(hist.keys()), log_val)
            plt.pause(0.01)
            if flatness(hist,acc):
                # End the algortihm if f gets small enough
                if f <= f_final:
                    return hist, f
                # Update f, reset hist, make a new inital config
                f = f**0.5
                hist = H(E_min,E_max,n_bins)
                model = config(l)

        # propose a move
        move = random_change(model)

        # Measure the energies for the moves
        E_1 = energy(model)
        E_2 = energy(move)

        # find bins
        index_1 = find_bin(hist, E_1)
        index_2 = find_bin(hist, E_2)

        # Determine whether or not to make the move and
        # alter the histogram accordingly
        if prob_flip(f, hist, index_1, index_2) >= random.random():
            update_hist(hist, index_2)
            model = move
        else:
            update_hist(hist, index_1)

        # Record the move
        check_counter += 1

    return hist, f

hist, f = wang_landau(16,40)
