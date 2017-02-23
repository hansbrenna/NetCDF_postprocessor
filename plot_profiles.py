# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 09:34:07 2017

@author: hanbre
"""

from __future__ import print_function
import sys
import netcdftime
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import matplotlib
from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import Normalize
import re
import seaborn as sns
import Ngl
#import HB_module.outsourced as outs


def vertical_interpolation(da,lev_n, hya, hyb, PS, P0):
    """This function operates on xarray.DataArray objects. Uses Ngl vinth2p.
    Give the original data, the pressure levels to interpolate to, the hybrid 
    coefficients, surface and reference pressure. Returns a DataArray object"""
    nlev = len(lev_n)
    dummy = np.empty(shape=[len(da.time),nlev,len(da.lat),len(da.lon)])
    time = da.time; lat = da.lat; lon = da.lon;
    dan = xr.DataArray(dummy,coords=[time, lev_n, lat, lon],dims=da.dims)
    dan.values = Ngl.vinth2p(da,hya,hyb,lev_n,PS,1,P0,1,False)
    return dan    

sns.set(font_scale=1.5)
sns.set_style('ticks')
avg = True
if avg:
    data=xr.open_mfdataset('f1850w.aCAVA_full.ens.anom.cam.h0.avg.????-????.T.hormean.nc',decode_times=False)
else:
    data=xr.open_mfdataset('f1850w.aCAVA_full.ens.anom.cam.h0.????.T.hormean.nc',decode_times=False)

ctr=xr.open_dataset('../../../new_control/f1850w.new_control.cam.h0.year.T.hormean.nc',decode_times=False)

T=data['T']
Tc = ctr['T']

plt.semilogy(Tc[0],Tc.lev,label='ctr')
ax = plt.gca()
ax.invert_yaxis()
plt.xlabel('Temperature (K)')
plt.ylabel('Model level (hPa)')
plt.legend()
plt.savefig('control_T_profile.png',bbox_inches='tight',dpi=300)
plt.show()


colors = sns.hls_palette(12,l=.3,s=.8)
for t in range(len(T.time)):
    plt.semilogy(T[t],T.lev,color=colors[t],label='{}'.format(t))

ax = plt.gca()
ax.invert_yaxis()
plt.xlabel('Temperature anomaly (K)')
plt.ylabel('Model level (hPa)')
plt.legend()
plt.savefig('experiment_T_profile.png',bbox_inches='tight',dpi=300)
plt.show()

