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

T = np.genfromtxt('T.dat')

print(T)

#create fig
fig = create_figure()
ax = create_single_panel(fig,xlabel="Temperature",ylabel="Delta S", palette=('viridis'))

# dirs = sorted(argv[1:], key=get_temp)
dirs = next(os.walk('.'))[1]
raw_size = list(map(get_sizes, dirs))

size = np.sort([x for x in raw_size if x!= 0])
print(size)

for s in size:
    line = np.abs(np.genfromtxt('final_models_l'+str(s)+'/delta_S.dat'))
    # ax.plot(T,line, label=str(s))
    ax.plot(line[:,0],line[:,1], label=str(s))
    # plt.plot(T,line)
    # plt.scatter(T,line)
plt.yscale('log')

# plt.xscale('log')
plt.legend()
plt.show()
plt.title("delta S and Temprature")
# plt.show()
finalize_and_save(fig, 'delta_S.pdf')
