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
ax = create_single_panel(fig,xlabel="Time",ylabel="Entropy",palette='cool',numcolors=len(dirs))

for direc in dirs:
    config.optionxform = str
    config.read(str(direc)+"/run.param")
    T = float(config['input']['T'])
    L = int(config['input']['l'])
    C = int(config['input']['C'])
    H = float(config['input']['H'])


    if data != "none": 
        df = pd.read_table(("S_T"+str(T)+".dat"),sep="\s+")
        df.columns = ['time', 's','std_err']
        t_space = np.array(df['time'])
        S = np.array(df['s'])
        std_err = np.array(df['std_err'])
        ax.errorbar(t_space,S,std_err,label = ("T="+str(T)))
    else:
        for direc in dirs:
            config.optionxform = str
            config.read(str(direc)+"/run.param")
            T = float(config['input']['T'])
            L = int(config['input']['l'])
            C = int(config['input']['C'])
            H = float(config['input']['H'])

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
                else:
                    S.append(float('nan'))
                    std_err.append(float('nan'))
            
            np.savetxt("S_T"+str(T)+".dat", np.c_[t_space,S,std_err])
            ax.errorbar(t_space,S,std_err,label = ("T="+str(T)))

    # plt.title("Cycle Entropy")
    # plt.legend()
    # plt.show()
# finalize_and_save(fig, 'chaotic_regime_entropy.pdf')
finalize_and_save(fig, 'test.pdf')
