# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:19:39 2016

@author: hanbre
"""
from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import xray
import matplotlib
import matplotlib.pyplot as plt
import scipy
import HB_module.outsourced as outs
import seaborn as sns

#fig= plt.figure(figsize=(12,6))

var='O3';pos='90S';p = -90

ensc = xray.open_dataset('files/f1850w.new_control.cam.h0.gases_antarctic_control_year.nc')
ens1 = xray.open_dataset('files/f1850w.aCAVA.ens1.cam.h0.gases.antarctic.strat.nc')
ens2 = xray.open_dataset('files/f1850w.aCAVA.ens2.cam.h0.gases.antarctic.strat.nc')
ens3 = xray.open_dataset('files/f1850w.aCAVA.ens3.cam.h0.gases.antarctic.strat.nc')
ens4 = xray.open_dataset('files/f1850w.aCAVA.ens4.cam.h0.gases.antarctic.strat.nc')
ens5 = xray.open_dataset('files/f1850w.aCAVA.ens5.cam.h0.gases.antarctic.strat.nc')

ensc = ensc.mean(dim='lon')
ens1 = ens1.mean(dim='lon')
ens2 = ens2.mean(dim='lon')
ens3 = ens3.mean(dim='lon')
ens4 = ens4.mean(dim='lon')
ens5 = ens5.mean(dim='lon')



timerange = range(31,39)
#timerange = range(35,47)
#timerange = range(0,59)

O3_c=getattr(ensc,var).sel(lat=p)
O3_1=getattr(ens1,var).sel(lat=p)
O3_2=getattr(ens2,var).sel(lat=p)
O3_3=getattr(ens3,var).sel(lat=p)
O3_4=getattr(ens4,var).sel(lat=p)
O3_5=getattr(ens5,var).sel(lat=p)

O3_c=xray.concat([O3_c,O3_c,O3_c,O3_c,O3_c],dim='time')

O3_c=O3_c.isel(time=timerange)
O3_1=O3_1.isel(time=timerange)
O3_2=O3_2.isel(time=timerange)
O3_3=O3_3.isel(time=timerange)
O3_4=O3_4.isel(time=timerange)
O3_5=O3_5.isel(time=timerange)

if 'BR' in var:
    O3_c=O3_c*1e9
    O3_1=O3_1*1e9
    O3_2=O3_2*1e9
    O3_3=O3_3*1e9
    O3_4=O3_4*1e9
    O3_5=O3_5*1e9
    unit='ppbv'
else:
    O3_c=O3_c*1e6
    O3_1=O3_1*1e6
    O3_2=O3_2*1e6
    O3_3=O3_3*1e6
    O3_4=O3_4*1e6
    O3_5=O3_5*1e6
    unit='ppmv'

fig=plt.figure(1)

O3_a = np.zeros((5,len(O3_1)))

O3_a[0,:]=O3_1.squeeze()
O3_a[1,:]=O3_2.squeeze()
O3_a[2,:]=O3_3.squeeze()
O3_a[3,:]=O3_4.squeeze()
O3_a[4,:]=O3_5.squeeze()

O3_m=np.mean(O3_a,axis=0)

plt.plot(O3_1,label='ens1')
plt.plot(O3_2,label='ens2')
plt.plot(O3_3,label='ens3')
plt.plot(O3_4,label='ens4')
plt.plot(O3_5,label='ens5')
plt.plot(O3_m,linewidth='3',label='ensm')
plt.plot(O3_c,linewidth='3',label='cntrl',color='k')


index,xtext=outs.parse_time_axis(ens1.time.isel(time=timerange),15)
plt.xticks(index.tolist(), xtext, size='larger')
locs, labels = plt.xticks()
plt.setp(labels, rotation=45)
plt.xlabel('Time',size='larger'); plt.ylabel('{0} concentration ({1})'.format(var,unit),size='larger')
plt.title('{0} at {1} 50 hPa'.format(var,pos))
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize=16)
plt.show()
fig.savefig('files/{0}_{1}_50hPa_{2}-{3}.png'.format(var,pos,xtext[0],xtext[-1]),bbox_inches='tight')