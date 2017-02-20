# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 14:07:25 2017
plot a separate colorbar
@author: hanbre
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as colors
from matplotlib.colors import Normalize

class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

fig = plt.figure(figsize=(8, 3))
ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])

clist = sns.diverging_palette(220, 20,n=10)
cmap = mpl.colors.ListedColormap(clist)
norm = MidpointNormalize(vmin=-200,vmax=200,midpoint=0)

ticks = [-200,-160,-120,-80,-40,0,40]
#ticks = None
clb = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                norm=norm,
                                orientation='horizontal',
                                ticks=ticks)
clb.ax.tick_params(labelsize=16)
clb.set_label('Column O3 anomaly (DU)',fontsize=18) 

fig.savefig('colorbar_anom.svg',bbox_inches='tight',dpi=300)