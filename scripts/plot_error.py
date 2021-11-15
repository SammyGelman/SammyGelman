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
home = str(Path.home())
def get_sizes(s):
    m = re.search(r'(?<=final_models_l)\w+', s)
    if not m:
        return 0
    return int(m.group(0))

#create fig
fig = create_figure()
ax = create_single_panel(fig,xlabel="System Size",ylabel="Mean Standard Error")

std_err = []

# dirs = sorted(argv[1:], key=get_temp)
dirs = next(os.walk('.'))[1]
raw_size = list(map(get_sizes, dirs))
size = [x for x in raw_size if x!= 0]

for s in size:
    std_err.append(np.mean(np.genfromtxt('final_models_l'+str(s)+'/error.dat')))
print(size)
print(std_err)
ax.plot(size,std_err)
plt.title("Mean Standard Error")
# plt.legend()
# plt.show()
finalize_and_save(fig, 'mean_std_err.pdf')
