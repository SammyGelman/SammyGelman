#!/usr/bin/python
import numpy as np 
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
from sys import argv
from scipy import interpolate
import configparser
import os
from matplotlib import cm
from figures import *
import argparse
import pandas as pd

dirs = next(os.walk('.'))[1]
# dirs = os.listdir()
# dirs = dirs[0:10]
config = configparser.ConfigParser()

#arg parser
parser = argparse.ArgumentParser()
parser.add_argument('resolution', type=int, nargs='+',
                    help='number of models trained on the cycle')
parser.add_argument('data', type=str, nargs='+',
                    help='data file -- write none if not yet generated.')
args = parser.parse_args()
resolution = args.resolution[0]
data = args.data[0]

#create fig
fig = create_figure()
ax = create_single_panel(fig,xlabel="Temp",ylabel="Entropy",palette='magma')

S_list=[]
T_list=[]



for direc in dirs:
    config.optionxform = str
    config.read(str(direc)+"/run.param")
    T = float(config['input']['T'])
    L = int(config['input']['l'])
    C = int(config['input']['C'])
    H = float(config['input']['H'])
    
    if data != "none":
        df = pd.read_table(str(data),sep="\s+")
        df.columns = ['temp', 's']
        S = np.array(df['s'])
        temp = np.array(df['temp'])
        ax.errorbar(temp,S,label = ("T="+str(T)))
    else:
        S=[] 
        std_err=[]
        # resolution = 10
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
            # else:
            #     S.append(float('nan'))
            #     std_err.append(float('nan'))
            #
        S_list.append(sum(S))
        T_list.append(T)

np.savetxt("Mean_S_Temp.dat", np.c_[T_list,S_list])
ax.plot(T_list,S_list)
plt.title("Mean Entropy")
# plt.legend()
# plt.show()
finalize_and_save(fig, 'mean_S_temp.pdf')
