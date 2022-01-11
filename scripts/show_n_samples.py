#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('samples', type=int, nargs='+',
                    help='number of samples to plot')
parser.add_argument('file', type=str, nargs='+',
                    help='file name')


args = parser.parse_args()
n = args.samples[0]
file_name = args.file[0]

# n=4
 
# if len(sys.argv) != 2:
#     print(f"Usage: {sys.argv[0]} <filename>")
#     exit(1)
#
# data = np.load(sys.argv[1])
data = np.load(file_name)
print(data['arr_0'].shape)

sn = int(np.sqrt(n))
data_n = []

for i in data.files[1:n]:
    data_n.append(data[i])

fig, ax = plt.subplots(sn, sn, sharex=True, sharey=True, subplot_kw={'xticks': [], 'yticks': []})

for i,(l, s) in enumerate(data.items()):
    if i == n:
        break
    else:
        x = i // sn
        # print(x)
        y = i % sn
        # print(y)
        ax[x, y].imshow(s, aspect='auto', vmin=-1, vmax=1)

plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig("samples.pdf")
plt.show()
