#!/usr/bin/python
import numpy as np 
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
from sys import argv
from scipy import interpolate
import configparser
import os

dirs = os.listdir()
dirs = dirs[0:10]
config = configparser.ConfigParser()

for direc in dirs:
    config.optionxform = str
    config.read(str(direc)+"/run.param")
    T = float(config['input']['T'])
    L = int(config['input']['l'])
    C = int(config['input']['C'])
    H = float(config['input']['H'])

    S=[] 
    std_err=[]
    resolution = 50
    times = int(C/resolution)
    t_space = times*(np.linspace(0,resolution-1,resolution))
    # t_space = np.delete(t_space, -1)
    
    for t in t_space:
        t = int(t)
        entropy_filename = 't'+str(t)+'_entropy.txt'
        print("Trying " + entropy_filename + "...")
        if os.path.isfile(str(direc) + '/' + entropy_filename):
            data = np.loadtxt(str(direc) + '/' + entropy_filename)
            print(data)
            if data.shape == ():
                data = data.reshape([1,])
            S.append(sum(data)/len(data))
            std_err.append(np.std(data))
        else:
            S.append(float('nan'))
            std_err.append(float('nan'))
    print(std_err)
    
    np.savetxt("S.dat", np.c_[t_space,S])
    plt.errorbar(t_space,S,std_err,label = ("T="+str(T)))
    plt.ylabel("Entropy")
    plt.xlabel("Time")

plt.title("Cycle Entropy")
plt.legend()
plt.show()
