#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import configparser
from sys import argv

dirs = argv[1:]

config = configparser.ConfigParser()
dir = sorted(dirs)

for direc in dirs:
    config.read(str(direc)+"/run.param")
    T = float(config['input']['T'])
    loss = np.loadtxt(str(direc)+'/loss.dat')
    plt.plot(loss[:,0],loss[:,1],label=str(T))
    # plt.plot(loss[0,:],loss[1,:],label=str(T))
    plt.legend()

plt.show()
