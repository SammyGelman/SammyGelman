import numpy as np
from analytic_entropy import onsager_entropy
import pandas as pd
import matplotlib.pyplot as plt
import configparser 

config = configparser.ConfigParser()
config.optionxform = str
config.read("run.param")
T = float(config['input']['T'])
H = float(config['input']['H'])
J = float(config['input']['J'])
C = int(config['input']['C'])


df = pd.read_table('curves.dat')
m = np.asarray(df['m'])
cycles = 3

entropy = []

for i in range(cycles*C):
    s = onsager_entropy(0.1,1,m[i],T)
    entropy.append(s)

np.savetxt("entropy_time.dat", np.c_[np.arange(0, len(entropy)),entropy])
plt.plot(m[0:cycles*C],entropy)
plt.show()
