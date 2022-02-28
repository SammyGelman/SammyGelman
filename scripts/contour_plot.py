#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import argparse

#arguments
parser = argparse.ArgumentParser()
parser.add_argument('x_axis',type=str, nargs='+',
                    help='x_axis values')
parser.add_argument('y_axis',type=str, nargs='+',
                    help='y_axis values')
parser.add_argument('data',type=str, nargs='+',
                    help='contour data')
args = parser.parse_args()

x_axis = np.genfromtxt(args.x_axis[0])
y_axis = np.genfromtxt(args.y_axis[0])
T = []
for t in y_axis:
    T.append(round(t,2))

print(T)
data = np.genfromtxt(args.data[0])

plot = plt.contourf(x_axis,y_axis,data, levels=200, cmap='turbo')
# plot = plt.contourf(x_axis,y_axis,data, levels=200, cmap='seismic')
plt.colorbar()
plt.savefig('contour_entropy.pdf')
plt.show()

