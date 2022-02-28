#!/usr/bin/env python
import numpy as np 
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
from sys import argv
import re
import os
from scipy import interpolate
from scipy import stats
from figures import *
import argparse 

#collect directories
home = str(Path.home())
def get_sizes(s):
    m = re.search(r'(?<=final_models_l)\w+', s)
    if not m:
        return 0
    return int(m.group(0))

#create fig
fig = create_figure()
ax = create_single_panel(fig,xlabel="System Size",ylabel="Delta S")

delta_S = []
error = []
# dirs = sorted(argv[1:], key=get_temp)
dirs = next(os.walk('.'))[1]
print(dirs)
raw_size = list(map(get_sizes, dirs))
print(raw_size)
size = np.sort([x for x in raw_size if x!= 0])

#remove 512 while problematic
size = np.delete(size,np.where(size == 512))

for s in size:
    delta_S.append(np.mean(np.abs(np.genfromtxt('final_models_l'+str(s)+'/delta_S.dat')[:,1])))
    error.append(np.mean(np.abs(np.genfromtxt('final_models_l'+str(s)+'/error.dat')[:,1])))
ax.plot(size,delta_S,color='red')
ax.errorbar(size,delta_S,yerr=error)
m,b = np.polyfit(np.log(size),np.log(delta_S),1)

print("The slope of our fit is: "+str(m))

y_fit = np.exp(m*np.log(size) + b)
ax.plot(size,y_fit)
# plt.plot(size,y_fit,color='blue')
# plt.plot(size,delta_S,color='red')
plt.scatter(size,delta_S,s=10)
plt.yscale('log')
plt.xscale('log')

chi_sq = stats.chisquare(delta_S,y_fit)
print(chi_sq)

plt.show()
plt.title("delta S and systemsize")
# plt.legend()
finalize_and_save(fig, 'delta_S.pdf')
