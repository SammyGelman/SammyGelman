import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def format_axes(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)

fig = plt.figure(constrained_layout=True)

gs = GridSpec(6, 6, figure=fig)

#Phase diagram l16
ax1 = fig.add_subplot(gs[0:3, 0:3])
#Phase diagram l32
ax2 = fig.add_subplot(gs[0:3, 3:6])
#Phase diagram l64
ax3 = fig.add_subplot(gs[3:4, 0:])

ax4 = fig.add_subplot(gs[4:5, 0:])
#magnetic feild/time
ax5 = fig.add_subplot(gs[5:6, 0:])

fig.suptitle("GridSpec")
format_axes(fig)

plt.show()
