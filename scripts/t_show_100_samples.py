#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <filename>")
    exit(1)

data = np.load(sys.argv[1])
n = 100
sn = int(np.sqrt(n))
data_n = []
l, s = list(data.items())[0]

for i in data.files[1:100]:
    data_n.append(s[i])

fig, ax = plt.subplots(sn, sn, sharex=True, sharey=True, subplot_kw={'xticks': [], 'yticks': []})

for i in range(len(s)):
    if i == n:
        break
    else:
        x = i // sn
        y = i % sn

        ax[x, y].imshow(s[i], aspect='auto', vmin=-1, vmax=1)
    

plt.subplots_adjust(wspace=0, hspace=0)
plt.show()
