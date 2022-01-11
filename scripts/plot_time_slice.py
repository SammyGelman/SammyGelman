#!/usr/bin/python
import numpy as np 
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
from sys import argv
import re
import os
from scipy import interpolate
from figures import *
import argparse 

#collect directories
T = np.genfromtxt('T.dat')

# #arguments
parser = argparse.ArgumentParser()
parser.add_argument('time', type=int, nargs='+',
                    help='size of model')
args = parser.parse_args()
time = args.time[0]


#create fig
fig = create_figure()
ax = create_single_panel(fig,xlabel="Temperature",ylabel="Entropy")

S=[] 

for temp in T:
    S.append(np.genfromtxt('S_T'+str(temp)+'.dat')[time,1])
print("This is T: "), print(T)
print("This is S: "), print(S)
# add on for temps 10 and 15

np.savetxt(str(time)+'_S.dat',S)

ax.plot(T,S)

finalize_and_save(fig, 'temperature_entropy_'+str(time)+".pdf")
plt.show()
