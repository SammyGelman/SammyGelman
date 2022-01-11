#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import re
import os
from scipy import interpolate
from figures import *
from onsager_solution import onsager_entropy
import glob

#collect directories
def get_temp(s):
    m = re.search(r'T(.*?)_', s)
    return float(m.group(1))

#create fig
fig = create_figure()
ax = create_horizontal_split(fig,2,merged=False,xlabel="Temperature",ylabel="Entropy")

S={}
std_err={}
# dirs = sorted(argv[1:], key=get_temp)
dirs = next(os.walk('.'))[1]
dirnames = glob.iglob('T*')
# T = list(map(get_temp, dirs))

# for dir in dirs:
#     # if 'batch_size2' in dir:
#     if 'T1.5' in dir:
#         entropy_filename = str(dir)+'/entropy.txt'
#         print("Trying " + entropy_filename + "...")
#         if os.path.isfile(entropy_filename):
#             data = np.loadtxt(entropy_filename)
#             if data.shape == ():
#                 data = data.reshape([1,])
#             # S.append(sum(data)/len(data))
#             S.append(sum(data[-1:])/1)
#             std_err.append(np.std(data))
#         else:
#             S.append(float('nan'))
#             std_err.append(float('nan'))
# # T = [1.5,2.0,2.5,3.0,3.5,4.0,4.5]
# T = [1.5,1.5]
#
# for dir in dirs:
#     entropy_filename = str(dir)+'/entropy.txt'
#     print("Trying " + entropy_filename + "...")
#     if os.path.isfile(entropy_filename):
#         data = np.loadtxt(entropy_filename)
#         if data.shape == ():
#             data = data.reshape([1,])
#         # S.append(sum(data)/len(data))
#         S.append(sum(data[-1:])/1)
#         std_err.append(np.std(data))
#     else:
#         S.append(float('nan'))
#         std_err.append(float('nan'))

for dirname in dirnames:
    # entropy_filename = str(dirname) + '/entropy.txt'
    entropy_filename = str(dirname) + '/final_entropy.txt'
    print("Trying " + entropy_filename + "...")
    if os.path.isfile(entropy_filename):
        # data = np.loadtxt(entropy_filename)[-1:]
        data = np.loadtxt(entropy_filename)
        T = get_temp(entropy_filename)
        S[T] = np.mean(data)
        std_err[T] = np.std(data)

# Get sorted data
data_T = np.array(list(sorted(S.keys())))
data_S = np.array(list(map(lambda T: S[T], data_T)))
data_std_err = np.array(list(map(lambda T: std_err[T], data_T)))

# fig, ax = plt.subplots(2, 1, sharex=True)

# Get analytical entropy
T_smooth = np.linspace(0.05, 15, 1500)
onsager_S_smooth = np.array(list(map(onsager_entropy, T_smooth)))
onsager_S_data_T = np.array(list(map(onsager_entropy, data_T)))
delta_S = data_S - onsager_S_data_T

# Save results
np.savetxt('S.dat', np.c_[data_T, data_S])
np.savetxt('error.dat', np.c_[data_T, data_std_err])
np.savetxt('delta_S.dat', np.c_[data_T, delta_S])
np.savetxt('onsager_S.dat', np.c_[T_smooth, onsager_S_smooth])

# Plot entropies
ax[0].plot(T_smooth, onsager_S_smooth)
ax[0].scatter(data_T, data_S)
ax[0].errorbar(data_T, data_S, yerr=data_std_err, fmt=' ')

# Plot and output entropy difference
ax[1].plot(data_T, delta_S)

finalize_and_save(fig, 'temperature_entropy.pdf')
plt.show()
