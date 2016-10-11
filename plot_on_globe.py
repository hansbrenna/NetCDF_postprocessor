# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 18:43:15 2016

@author: hanbre
"""

from __future__ import print_function
import sys
import netcdftime
import numpy as np
import pandas as pd
import xarray
import netCDF4
from mpl_toolkits.basemap import Basemap, shiftgrid
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import Normalize
import re
import seaborn as sns
import HB_module.outsourced as outs

file_id = sys.argv[1]
variable = sys.argv[2]



ds=xarray.open_dataset(file_id)



x = ds.lon; y = ds.lat
clevels=None
cmap=sns.cubehelix_palette(light=1, as_cmap=True)
norm=None
var = getattr(ds,variable)


map = Basemap(projection = 'cyl',llcrnrlat=-30,urcrnrlat=30,llcrnrlon=0,urcrnrlon=360,resolution='l')#projection='splaea',boundinglat=-45,lon_0=270,resolution='l')#(projection='ortho',lat_0=60.,lon_0=-60.)#projection = 'cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='l')
map.drawcoastlines(linewidth=0.25)
meridians = map.drawmeridians(np.arange(0,360,30))
map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=14)
parallels = map.drawparallels(np.arange(-80,81,20))
map.drawparallels(parallels,labels=[1,0,0,0],fontsize=14)

lons, lats = np.meshgrid(x,y)
mx,my = map(lons,lats)
CF = map.contourf(mx,my,var,cmap=cmap) 
CS = map.contour(mx,my,var,np.linspace(200,200,1),colors='k')
plt.colorbar(CF)

fig=plt.figure()
#lons, lats = np.meshgrid(x,y)
#var, lons = shiftgrid(lon0 = 300., datain =var , lonsin = lons, start = True, cyclic = 360.)
map = Basemap(projection='ortho',lat_0=-60,lon_0=180,resolution='l')#(projection='hammer',lon_0=180,resolution='c')#Basemap(projection='spaeqd',boundinglat=-10,lon_0=270,resolution='l')#(projection='splaea',boundinglat=-45,lon_0=270,resolution='l')#(projection='ortho',lat_0=60.,lon_0=-60.)#projection = 'cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='l')
map.drawcoastlines(linewidth=0.25)
meridians = map.drawmeridians(np.arange(0,360,30))
map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=14)
parallels = map.drawparallels(np.arange(-80,81,20))
map.drawparallels(parallels,labels=[1,0,0,0],fontsize=14)

mx,my = map(lons,lats)
CF = map.contourf(mx,my,var,np.linspace(120,420,16),cmap=cmap) 
CS = map.contour(mx,my,var,np.linspace(200,200,1),colors='k')
clb=plt.colorbar(CF)
clb.set_label('Column O3 (DU)',fontsize=18)
timestamp=outs.make_timestamp(file_id)
plt.title('Column O3 Time: {0}'.format(timestamp),fontsize=18)
#plt.show()
fig.savefig('{0}_ozone_hole.png'.format(file_id),bbox_inches='tight')

