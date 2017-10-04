#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 09:19:46 2017

@author: hanbre
"""
from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib import colors as c
import seaborn
from scipy import stats
from scipy.stats import ttest_ind,ranksums

normality_check = False    

control = xr.open_dataset('/home/hanbre/nird/BCKUP_after_21.07.15/new_control_test/f1850w.new_control.cam.h0.DJFe.nc',decode_times=False)
experiment = xr.open_dataset('/home/hanbre/nird/BCKUP_after_21.07.15/aCAVA_experiment/PV_dynamics_significant/f1850w.aCAVA_full.ense.cam.h0.UT.DJF1.nc')

cU = control['T']
eU = experiment['T']

cUm = cU.mean(dim = ['time','lon'])
dummy = cUm.mean(dim = 'record')
mcU = dummy.copy(deep=True)
eUm = eU.mean(dim = ['time','lon'])
meU = eUm.mean(dim = 'record')
anom = meU-mcU

lev = control.lev
lat = control.lat

rdata = np.zeros([cUm.shape[1],cUm.shape[2]])
r = xr.DataArray(rdata,coords=dummy.coords,dims=dummy.dims)
cnormality = r.copy(deep=True)
enormality = r.copy(deep=True)
#it = 0
for la in lat:
    for le in lev:
        if normality_check:
            cnorm_temp = stats.shapiro(cUm.loc[dict(lat=la,lev=le)])
            cnormality.loc[dict(lat=la,lev=le)] = cnorm_temp[1]
            enorm_temp = stats.shapiro(eUm.loc[dict(lat=la,lev=le)])
            enormality.loc[dict(lat=la,lev=le)] = enorm_temp[1]
        r_temp = (stats.ranksums(cUm.loc[dict(lat=la,lev=le)],eUm.loc[dict(lat=la,lev=le)]))
#        r_temp = ttest_ind(cUm.loc[dict(lat=la,lev=le)],eUm.loc[dict(lat=la,lev=le)],equal_var=False)
        r.loc[dict(lat=la,lev=le)] = r_temp.pvalue
#        print(eUm.loc[dict(lat=la,lev=le)].values)
#        it = it + 1
#        if it ==100:
#            sys.exit()

temp1 = r.copy(deep=True)
temp2 = temp1.where(temp1<0.05)
temp3 = temp2.fillna(-999)
temp4 = temp3.where(temp3 == -999)
temp5 = temp4.fillna(1.)
temp6 = temp5.where(temp5 != -999)
sig95 = temp6.fillna(0.0)


X,Y = np.meshgrid(lat,lev)

cmap=c.ListedColormap(['white','white','white'])

plt.figure()
anom.plot.contourf(levels = np.linspace(-12,12,9))
#plt.yscale('log')
#plt.gca().invert_yaxis()
plt.hold('on')
#sig95.plot.contourf(cmap=cmap,levels=[0,0.1,1],hatches=['','+'],alpha=0.7)
plt.contourf(lat,lev,sig95,cmap=cmap,levels=[0,0.1,1],hatches=['','..'],alpha=0.)
#plt.pcolor(X,Y,sig95,cmap=cmap,hatch='/',alpha=0.01)
plt.yscale('log')
plt.gca().invert_yaxis()
plt.show()
