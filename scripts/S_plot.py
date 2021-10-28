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

temps = np.genfromtxt("T.dat")

#create fig
fig = create_figure()
ax = create_single_panel(fig,xlabel="Time",ylabel="Entropy",palette='cool',numcolors=len(temps))

for T in temps: 
    df = pd.read_table(("S_T"+str(T)+".dat"),sep="\s+")
    df.columns = ['time', 's','std_err']
    t_space = np.array(df['time'])
    S = np.array(df['s'])
    std_err = np.array(df['std_err'])
    ax.errorbar(t_space,S,std_err,label = ("T="+str(T)))

# finalize_and_save(fig, 'chaotic_regime_entropy.pdf')
finalize_and_save(fig, 'test.pdf')
