import numpy as np
import os
import matplotlib.pyplot as plt
import re

dirs = os.listdir()

def get_temp(s):
    m = re.search(r'T(.*?)_', s)
    return float(m.group(1))  

T = list(map(get_temp, dirs)) 
print(T)
S = []
std_err=[]
C=50

resolution = 50
correction = C/resolution
t_space = correlation*np.linspace(0,resolution-1,resolution)

for d in dirs: 
    entropy_filename = str(d)+'/entropy.txt' 
    if os.path.isfile(entropy_filename): 
        data = np.loadtxt(entropy_filename) 
        if data.shape == (): 
            data = data.reshape([1,])
        S.append(sum(data)/len(data))
        std_err.append(np.std(data))
    else: 
        S.append(float('nan'))
        std_err.append(float('nan'))

plt.plot(T,S)
plt.show()


