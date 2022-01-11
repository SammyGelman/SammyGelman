#!/usr/bin/python
import numpy as np 
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
from sys import argv
from scipy import interpolate
import configparser
import os

config = configparser.ConfigParser()
config.optionxform = str
config.read("run.param")
T = float(config['input']['T'])
L = int(config['input']['l'])
C = int(config['input']['C'])
H = float(config['input']['H'])

S=[] 
std_err=[]
resolution = 50
times = int(C/resolution)
t_space = times*(np.linspace(0,resolution-1,resolution))
print(t_space)

for t in t_space:
    t = int(t)
    entropy_filename = 't'+str(t)+'_entropy.txt'
    print("Trying " + entropy_filename + "...")
    if os.path.isfile(entropy_filename):
        data = np.loadtxt(entropy_filename)
        print(data)
        if data.shape == ():
            data = data.reshape([1,])
        S.append(sum(data)/len(data))
        std_err.append(np.std(data))
    else:
        S.append(float('nan'))
        std_err.append(float('nan'))
print(S)
np.savetxt("S.dat", np.c_[t_space,S])
fig = plt.plot(t_space,S)
plt.show()
