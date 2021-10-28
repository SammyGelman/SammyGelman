# !/usr/bin/env python
"""
Nice publication quality figures. See examples for usage.
"""
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pgf import FigureCanvasPgf
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from matplotlib.ticker import LinearLocator, AutoLocator, FixedLocator
from matplotlib.colors import LinearSegmentedColormap

matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)

cm_in_inches = 0.393701
golden_ratio = 1.61803398875

plt.rcParams.update({
    "font.family": "serif",  # use serif/main font for text elements
    "text.usetex": True,     # use inline math for ticks
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.preamble": "\n".join([
         r"\usepackage{url}",                        # load additional packages
         r"\usepackage{unicode-math}",               # unicode math setup
         r"\setmainfont{DejaVu Serif}",              # serif font via preamble
         r"\usepackage[Symbolsmallscale]{upgreek}",  # Uppercase greek
    ])
})

plt.rc('font', **{'family':'serif', 'serif':['Times'], 'size': 9.0})
plt.rc('lines', linewidth=0.5)
plt.rc('axes', linewidth=0.5)
plt.rc('xtick', labelsize='medium', direction='in')
plt.rc('ytick', labelsize='medium', direction='in')
plt.rc('xtick.major', size=4.0, width=0.5)
plt.rc('xtick.minor', size=2.0, width=0.5)
plt.rc('ytick.major', size=4.0, width=0.5)
plt.rc('ytick.minor', size=2.0, width=0.5)
plt.rc('legend', fontsize='small', loc='best')
plt.rc('text', usetex=True)

# Custom diverging colormap for white background:
cdict_blrddark = {
			'red':   ((0.0, 0.0, 0.0),
                     (0.5, 0.0, 0.0),
                     (1.0, 1.0, 1.0)),

			'green': ((0.0, 0.0, 0.0),
                     (1.0, 0.0, 0.0)),

			'blue':  ((0.0, 0.0, 1.0),
                     (0.5, 0.0, 0.0),
                     (1.0, 0.0, 0.0))
			}
cdict_rdbldark = {
			'red':   ((0.0, 1.0, 1.0),
                     (0.5, 0.0, 0.0),
                     (1.0, 0.0, 0.0)),

			'green': ((0.0, 0.0, 0.0),
                     (1.0, 0.0, 0.0)),

			'blue':  ((0.0, 0.0, 0.0),
                     (0.5, 0.0, 0.0),
                     (1.0, 1.0, 1.0))
			}
matplotlib.cm.register_cmap("BlRdDark", LinearSegmentedColormap("BlRdDark", cdict_blrddark))
matplotlib.cm.register_cmap("RdBlDark", LinearSegmentedColormap("RdBlDark", cdict_rdbldark))

# plotting:


def filled_plot(ax, x, y1, y2, linestyle="solid", alpha=0.5, linealpha=1.0, linewidth=1.0, label=None):
    base_line, = ax.plot(x, y1, linestyle=linestyle, linewidth=linewidth, label=label, alpha=linealpha)
    color = base_line.get_color()
    ax.plot(x, y2, color=color, linestyle=linestyle, linewidth=linewidth, alpha=linealpha)
    ax.fill_between(x, y1, y2, color=color, linestyle=linestyle, alpha=alpha, linewidth=linewidth)


# def filled_error_plot(ax, x, y, err, linestyle ="solid", alpha=0.5, linealpha=1.0, linewidth=1.0, label=None):
#     filled_plot(ax, x, y-err, y+err, linestyle, alpha, linealpha, linewidth, label)

def filled_region(ax, x, y1, y2, color, linestyle="solid", alpha=0.5, linealpha=1.0, linewidth=1.0, label=None):
    ax.fill_between(x, y1, y2, color=color, linestyle=linestyle, alpha=alpha, linewidth=linewidth)

def filled_error_plot(ax, x, y, err, linestyle="solid", alpha=0.5, linealpha=1.0, linewidth=1.0, label=None):
    base_line, = ax.plot(x, y, linestyle=linestyle, alpha=linealpha, linewidth=linewidth, label=label)
    color = base_line.get_color()
    filled_region(ax, x, y-err, y+err, color, linestyle, alpha, linealpha=0.0, linewidth=0.0, label=None)

def create_figure(width_inches=None, height_inches=None, height_multiplier=None):
    fig = plt.figure()
    fig.horizontal_merged = False
    fig.vertical_merged = False
    if width_inches is None:
        width_inches = 8.6 * cm_in_inches
    fig.default_height = width_inches / golden_ratio
    if height_inches is None:
        height_inches = fig.default_height
    if height_multiplier is not None:
        height_inches *= height_multiplier
    fig.set_size_inches(width_inches, height_inches)
    return fig


def set_default_spacing(fig):
    # These are a good start in most cases, but may require some manual adjustment.
    fig.subplots_adjust(bottom=0.17 * fig.default_height / fig.get_size_inches()[1])
    fig.subplots_adjust(left=0.14)
    fig.subplots_adjust(top=1.0 - 0.02 * fig.default_height / fig.get_size_inches()[1])
    fig.subplots_adjust(right=0.97)


def create_single_panel(fig,
                        xlabel=None,
                        ylabel=None,
                        palette='Set1',
                        numcolors=9):
    ax = fig.add_subplot(111)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
        fig.subplots_adjust(bottom=0.2)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    ax.set_prop_cycle('color', plt.get_cmap(palette)(np.linspace(0,1,numcolors)))
    set_default_spacing(fig)
    return ax

# This is an Nx1 plot, with the axes merged by default.
def create_horizontal_split(fig, N, merged=True, xlabel=None, ylabel=None, palette=None, numcolors=None):
    if palette is None:
        palette = ['Set1'] * N
    if numcolors is None:
        numcolors = [9] * N
    axes = fig.subplots(nrows=N, ncols=1,sharex=merged)
    if merged: # Axes are merged
        fig.horizontal_merged = True
        fig.subplots_adjust(hspace=0)
        if xlabel is not None:
            axes[-1].set_xlabel(xlabel[-1])
    else: # Axes are unmerged
        fig.horizontal_merged = False
        if xlabel is not None:
            for i, ax in enumerate(axes):
                ax.set_xlabel(xlabel[i])
        fig.subplots_adjust(hspace=0.5)
    # Axes are either merged or unmerged
    if ylabel is not None:
        for i, ax in enumerate(axes):
            ax.set_ylabel(ylabel[i])

    for i, ax in enumerate(axes):
        ax.set_prop_cycle('color', plt.get_cmap(palette[i])(np.linspace(0,1,numcolors[i])))
    set_default_spacing(fig)
    return axes

# This is a 2x1 plot, with the axes merged by default.
# TODO: Can be generalized to Nx1.
def create_vertical_split(fig,
                          merged=True,
                          xlabel=None,
                          ylabel=None,
                          palette=('Set1', 'Set1'),
                          numcolors=(9, 9)):
    ax1 = fig.add_subplot(121)

    if merged:
        fig.vertical_merged = True
        ax2 = fig.add_subplot(122, sharey=ax1)  # Share axes.
        fig.subplots_adjust(wspace=0)  # Merge axes.
        plt.setp(
            [a.get_yticklabels()
             for a in fig.axes[1:]], visible=False)  # Remove ticks from right axes.
        if ylabel is not None:
            ax1.set_ylabel(ylabel[0])  # No ylabel for right axes.
    else:
        fig.vertical_merged = False
        ax2 = fig.add_subplot(122)
        if ylabel is not None:
            ax1.set_ylabel(ylabel[0])
            ax2.set_ylabel(ylabel[1])
        fig.subplots_adjust(wspace=0.5)
    if xlabel is not None:
        ax1.set_xlabel(xlabel[0])
        ax2.set_xlabel(xlabel[1])

    ax1.set_prop_cycle('color', plt.get_cmap(palette[0])(np.linspace(0, 1, numcolors[0])))
    ax2.set_prop_cycle('color', plt.get_cmap(palette[1])(np.linspace(0, 1, numcolors[1])))
    set_default_spacing(fig)
    return ax1, ax2

# This is a 2x2 plot, with the axes always merged.
# TODO: Can be generalized to NxM, partially merged.
def create_quad_split(fig,
                      xlabel=None,
                      ylabel=None,
                      palette=('Set1', 'Set1', 'Set1', 'Set1'),
                      numcolors=(9, 9, 9, 9),
                      tight_layout=True):

    fig.horizontal_merged = True
    fig.vertical_merged = True
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222, sharey=ax1)
    ax3 = fig.add_subplot(223, sharex=ax1)
    ax4 = fig.add_subplot(224, sharey=ax3)

    # Merge axes.
    fig.subplots_adjust(wspace=0)
    fig.subplots_adjust(hspace=0)

    # Remove ticks from top axes.
    for p in [0, 1]:
        plt.setp(fig.axes[p].get_xticklabels(), visible=False)
    # Remove ticks from right axes.
    for p in [1, 3]:
        plt.setp(fig.axes[p].get_yticklabels(), visible=False)

    # Set axis labels.
    if xlabel is not None:
        ax3.set_xlabel(xlabel[0])
        ax4.set_xlabel(xlabel[1])
    if ylabel is not None:
        ax1.set_ylabel(ylabel[0])
        ax3.set_ylabel(ylabel[1])

    for i, ax in enumerate([ax1, ax2, ax3, ax4]):
        ax.set_prop_cycle('color', plt.get_cmap(palette[i])(np.linspace(0, 1, numcolors[i])))
    set_default_spacing(fig)
    return ax1, ax2, ax3, ax4

"""
Create the final figure and save it to file.

:param fig: The Figure object to use.
:param filename: The file name to save to.
:param legend_axes: The indices of axes in which to place a legend.
"""
def finalize_and_save(fig, filename='plot.pdf', legend_axes=[0], dpi=400, leg_col=None, remove_internal_labels=True):
    axes = fig.get_axes()
    if leg_col is None:
        leg_col = [1] * len(axes)
    for i, ax in enumerate(axes):
        if legend_axes is not None:
            if i in legend_axes:
                legend = ax.legend(loc='best', fancybox=True, framealpha=0.8, ncol=leg_col[i], handlelength=0.5)
                if legend is not None:
                    legend.get_frame().set_linewidth(0.5)
        ax.minorticks_on()
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.margins(0)
    if remove_internal_labels:
        if fig.vertical_merged and not fig.horizontal_merged:
            plt.setp(
                [a.get_xticklabels()[-1]
                for a in fig.axes[:-1]], visible=False)  # Remove last label from left axes.
        if fig.horizontal_merged and not fig.vertical_merged:
            plt.setp(
                [a.get_yticklabels()[-1]
                for a in fig.axes[1:]], visible=False)  # Remove last label from bottom axes.
        if fig.horizontal_merged and fig.vertical_merged:
            plt.setp(fig.axes[2].get_yticklabels()[-1], visible=False)
            plt.setp(fig.axes[2].get_xticklabels()[-1], visible=False)
    fig.savefig(filename, dpi=dpi)
