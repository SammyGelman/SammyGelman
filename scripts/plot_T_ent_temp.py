#!/usr/bin/python
import numpy as np 
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
from sys import argv
import re
import os
from scipy import interpolate

# home = str(Path.home())
def get_temp(s):
    m = re.search(r'T(.*?)_', s)
    return float(m.group(1))

S=[] 
std_err=[]
dirs = sorted(argv[1:], key=get_temp)
T = list(map(get_temp, dirs))
for dir in dirs:
    entropy_filename = str(dir)+'/entropy.txt'
    print("Trying " + entropy_filename + "...")
    if os.path.isfile(entropy_filename):
        data = np.loadtxt(entropy_filename)
        if data.shape == ():
            data = data.reshape([1,])
        S.append(sum(data)/len(data))
        std_err.append(np.std(data))
    else:
        S.append(float('nan'))
        std_err.append(float('nan'))

onsager_S = pickle.load( open("/gcohenlab/data/samuelgelman/src/analytical_results/S_analytical.pkl", "rb" ) )
onsager_T = pickle.load( open("/gcohenlab/data/samuelgelman/src/analytical_results/Ts_fine.pkl", "rb" ) )

print(onsager_T)

print("This is T: "), print(T)
print("This is S: "), print(S)
T,S=T[0:-2],S[0:-2]
print(len(S),len(T))
def specific_temps(T,onsager_T,onsager_S):
    specific_T = []
    specific_S = []
    for temp in T:
        for o_temp in range(len(onsager_T)):
            if temp <= onsager_T[o_temp]:
                specific_T.append(onsager_T[o_temp])
                specific_S.append(onsager_S[o_temp])
                break
    return specific_T, specific_S

specific_T, specific_S = specific_temps(T,onsager_T,onsager_S)

print(len(specific_S))

fig, axs = plt.subplots(2, 1, sharex=True)

axs[0].plot(onsager_T,onsager_S)
axs[0].scatter(T,S)
# axs[0].errorbar(T,S,yerr=std_err,fmt=' ')


# Sfunc = interpolate.interp1d(T, S)
# S_interpolated = Sfunc(onsager_T)
# axs[1].plot(onsager_T, S_interpolated - onsager_S)

print(len(S))
S_dif = []
for i in range(len(S)):
    S_dif.append(S[i] - specific_S[i])

axs[1].plot(T, S_dif)

fig.savefig("Entropy_Temp_Graph.pdf")
plt.show()
