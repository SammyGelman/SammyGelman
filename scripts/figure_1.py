import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def format_axes(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)

fig = plt.figure(constrained_layout=True)

gs = GridSpec(4, 4, figure=fig)

#delta S, T for different sample sizes
ax1 = fig.add_subplot(gs[0:2, 0:2])
#T0.05 - real
ax2 = fig.add_subplot(gs[0, 2])
#T0.05 - synthetic
ax3 = fig.add_subplot(gs[0, 3])
#T1.5 - real
ax4 = fig.add_subplot(gs[1, 2])
#T1.5 - synthetic
ax5 = fig.add_subplot(gs[1, 3])
#mean delta S for different system sizes
ax6 = fig.add_subplot(gs[2:4, 0:2])
#T2.5 - real
ax7 = fig.add_subplot(gs[2, 2])
#T2.5 - synthetic
ax8 = fig.add_subplot(gs[2, 3])
#T4.5 - real
ax9 = fig.add_subplot(gs[3, 2])
#T4.5 - synthetic
ax10 = fig.add_subplot(gs[3, 3])

# identical to ax1 = plt.subplot(gs.new_subplotspec((0, 0), colspan=3))
fig.suptitle("GridSpec")
format_axes(fig)

plt.show()
