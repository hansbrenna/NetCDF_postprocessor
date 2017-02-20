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
import HB_module.outsourced as outs



data=xr.open_mfdataset('f1850w.aCAVA_full.ens.anom.cam.h0.*.T.hormean.nc',decode_times=False)
ctr=xr.open_dataset('../../../new_control/f1850w.new_control.cam.h0.year.T.hormean.nc',decode_times=False)

T=data['T']
Tc = ctr['T']

plt.semilogy(Tc[0],Tc.lev)
ax = plt.gca()
ax.invert_yaxis()
plt.xlabel('Temperature (K)')
plt.ylabel('Model level (hPa)')
plt.show()


for t in range(len(T.time)):
    plt.semilogy(T[t],T.lev)

ax = plt.gca()
ax.invert_yaxis()
plt.xlabel('Temperature anomaly (K)')
plt.ylabel('Model level (hPa)')
plt.show()

