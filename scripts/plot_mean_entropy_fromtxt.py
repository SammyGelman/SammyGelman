import numpy as np
import matplotlib.pyplot as plt
import argparse
from figures import *

#create fig
fig = create_figure()
ax = create_single_panel(fig,xlabel="Temp",ylabel="Entropy",palette='magma')

#arguments
parser = argparse.ArgumentParser()
parser.add_argument('x_axis',type=str, nargs='+',
                    help='x_axis values')
parser.add_argument('y_axis',type=str, nargs='+',
                    help='y_axis values')
args = parser.parse_args()

x_axis = np.genfromtxt(args.x_axis[0])
y_axis = np.genfromtxt(args.y_axis[0])

ax.plot(x_axis,y_axis)
plt.title("Mean Entropy")
# plt.legend()
# plt.show()
finalize_and_save(fig, 'mean_S_temp.pdf')
