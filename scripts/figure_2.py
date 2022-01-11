import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

def format_axes(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)

fig = plt.figure(constrained_layout=True)

gs = GridSpec(6, 6, figure=fig)

#Phase diagram l16
ax1 = fig.add_subplot(gs[0:2, 0:3])
#Phase diagram l32
ax2 = fig.add_subplot(gs[0:2, 3:6])
#Phase diagram l64
ax3 = fig.add_subplot(gs[2:4:, 0:3])
#magnetic feild/time
ax4 = fig.add_subplot(gs[4:6, 0:3])
#stuck
ax5 = fig.add_subplot(gs[-4, 3:])
#linear response
ax6 = fig.add_subplot(gs[-3, 3:])
#saturated
ax7 = fig.add_subplot(gs[-2, 3:])
#chaotic regime
ax8 = fig.add_subplot(gs[-1, 3:])



#test a sin wave on subplot
def f(x):
    return np.sin(x)
x = np.linspace(0,2*np.pi,100)
ax8.plot(x,f(x))
# fig.suptitle("GridSpec")
format_axes(fig)

plt.show()
