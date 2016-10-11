# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 16:26:41 2016

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
try :
    sys.argv[2]
    if sys.argv[2] == 'tl':
        tl = True
    else:
        tl = False
except IndexError:
    tl = False

ds =xarray.open_dataset(file_id)
ds
ds.O3
O3_vmm = ds.O3
O3_mmm = O3_vmm*(48.0/28.94)

g=9.81
P0 = ds.P0
PS = ds.PS
hyai = ds.hyai
hybi = ds.hybi
Plevi = hyai*P0+hybi*PS

dp = np.empty(shape=O3_vmm.shape)

dpa=xarray.DataArray(dp,coords=ds.O3.coords,dims=ds.O3.dims)

for i in range(1,Plevi.shape[0]):
    dpa[dict(lev=i-1)]=Plevi[i]-Plevi[i-1]
    
O3_t=O3_mmm*dpa/g

totO3=O3_t.sum(dim='lev')

totO3DU = totO3/2.1415e-5

ds2=totO3DU.to_dataset(name='totO3')
ds3=ds.merge(ds2)
ds3.totO3.attrs['units']='DU'
ds3.totO3.attrs['long_name']='Column ozone in Dobson Units'

x = ds3.lon; y = ds3.lat
clevels=None
cmap=sns.cubehelix_palette(light=1, as_cmap=True)
norm=None
var = ds3.totO3.isel(time=0)

if tl == True:
    fig_tl = plt.figure()
    var = ds3.totO3.mean(dim='lon')
    var['time']=np.arange(var.time.shape[0])
#    var.plot.contourf(x='time',y='lat',cmap=cmap)
    CF=plt.contourf(var.time,var.lat,var.transpose(),np.linspace(120,460,18),cmap=cmap)
    plt.contour(var.time,var.lat,var.transpose(),np.linspace(200,200,1),colors='k')
    plt.colorbar(CF) 
    #plt.show()
    fig_tl.savefig('{0}_ozone_timelat.png'.format(file_id),bbox_inches='tight')
else:
    fig_map=plt.figure()
    map = Basemap(projection = 'cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='l')#projection='splaea',boundinglat=-45,lon_0=270,resolution='l')#(projection='ortho',lat_0=60.,lon_0=-60.)#projection = 'cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='l')
    map.drawcoastlines(linewidth=0.25)
    meridians = map.drawmeridians(np.arange(0,360,30))
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=14)
    parallels = map.drawparallels(np.arange(-80,81,20))
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=14)
    
    lons, lats = np.meshgrid(x,y)
    mx,my = map(lons,lats)
    CF = map.contourf(mx,my,var,np.linspace(120,460,18),cmap=cmap) 
    CS = map.contour(mx,my,var,np.linspace(200,200,1),colors='k')
    plt.colorbar(CF)
    fig_map.savefig('{0}_ozone_map.png'.format(file_id),bbox_inches='tight')
    
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
    CF = map.contourf(mx,my,var,np.linspace(120,460,18),cmap=cmap)#np.linspace(120,420,16),cmap=cmap) 
    CS = map.contour(mx,my,var,np.linspace(200,200,1),colors='k')
    clb=plt.colorbar(CF)
    clb.set_label('Column O3 (DU)',fontsize=18)
    try:
        timestamp=outs.make_timestamp(file_id)
    except:
        timestamp = 'dummy'
    plt.title('Column O3 Time: {0}'.format(timestamp),fontsize=18)
    #plt.show()
    fig.savefig('{0}_ozone_hole.png'.format(file_id),bbox_inches='tight')
