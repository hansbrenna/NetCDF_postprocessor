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

fig = plt.figure(figsize=(8, 3))
ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])

clist = sns.cubehelix_palette(18,start=.5, rot=-.75)
cmap = mpl.colors.ListedColormap(clist)
norm = mpl.colors.Normalize(vmin=100, vmax=460)

ticks = [100,140,180,220,260,300,340,380,420,460]
#ticks = None
clb = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                norm=norm,
                                orientation='horizontal',
                                ticks=ticks)
clb.ax.tick_params(labelsize=16)
clb.set_label('Column O3 (DU)',fontsize=18) 

fig.savefig('colorbar',bbox_inches='tight',dpi=300)