#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <filename>")
    exit(1)

data = np.load(sys.argv[1])
data = data[data.files[0]][:,:,:,0]
data = np.where(data == 0, -1, 1)
n = 4
sn = int(np.sqrt(n))
data_n = []
# l, s = list(data.items())[0]

for i in range(n):
    data_n.append(data[i,:,:])

fig, ax = plt.subplots(sn, sn, sharex=True, sharey=True, subplot_kw={'xticks': [], 'yticks': []})

# for i,(l, s) in enumerate(data.items()):
for i in range(len(data_n)):
    if i == n:
        break
    else:
        x = i // sn
        y = i % sn
        ax[x, y].imshow(data_n[i], aspect='auto', vmin=-1, vmax=1)
    

plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig("samples.pdf")
plt.show()
