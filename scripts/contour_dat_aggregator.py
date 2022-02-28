#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
from sys import argv
from scipy import interpolate
import configparser
import os
import argparse

dirs = next(os.walk('.'))[1]
# dirs = os.listdir()
# dirs = dirs[0:10]

config = configparser.ConfigParser()

resolution = 50

S_list=[]
T_list=[]
contour_dat = np.zeros((len(dirs),resolution))
error_dat = np.zeros((len(dirs),resolution))
i=0

def sort_func(direc):
    config.optionxform = str
    config.read(str(direc)+"/run.param")
    T = float(config['input']['T'])
    return T



for direc in sorted(dirs, key=sort_func):
    config.optionxform = str
    config.read(str(direc)+"/run.param")
    T = float(config['input']['T'])
    L = int(config['input']['l'])
    C = int(config['input']['C'])
    H = float(config['input']['H'])

    print("Collecting for dir "+str(direc))

    S=[]
    std_err=[]
    # resolution = 10
    times = int(C/resolution)
    t_space = times*(np.linspace(0,resolution-1,resolution))
    # t_space = np.delete(t_space, -1)
    for t in t_space:
        t = int(t)
        entropy_filename = 't'+str(t)+'_entropy.txt'
        if os.path.isfile(str(direc) + '/' + entropy_filename):
            data = np.loadtxt(str(direc) + '/' + entropy_filename)
            if data.shape == ():
                data = data.reshape([1,])
            S.append(sum(data)/len(data))
            contour_dat[i,t]=(sum(data)/len(data))
            error_dat[i,t]=np.std(data)

    # for t in t_space:
    #     if t >= 20 and t<=33:
    #         t = int(t)
    #         entropy_filename = 't'+str(t)+'_entropy.txt'
    #         print("Trying " + entropy_filename + "...")
    #         if os.path.isfile(str(direc) + '/' + entropy_filename):
    #             data = np.loadtxt(str(direc) + '/' + entropy_filename)
    #             if data.shape == ():
    #                 data = data.reshape([1,])
    #             S.append(sum(data)/len(data))
    #             std_err.append(np.std(data))
        # else:
        #     S.append(float('nan'))
        #     std_err.append(float('nan'))
        #
    i+=1
    print(T)
    T_list.append(T)
    print(T_list)
np.savetxt('contour.dat',contour_dat)
np.savetxt('T.dat',T_list)
np.savetxt('error.dat',error_dat)
