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

ensc = xray.open_dataset('files/f1850w.new_control.cam.h0.gases_antarctic_control_10-04.nc')
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

O3_c=ensc.O3.sel(lat=-90)
O3_1=ens1.O3.sel(lat=-90)
O3_2=ens2.O3.sel(lat=-90)
O3_3=ens3.O3.sel(lat=-90)
O3_4=ens4.O3.sel(lat=-90)
O3_5=ens5.O3.sel(lat=-90)

O3_1=O3_1.isel(time=timerange)
O3_2=O3_2.isel(time=timerange)
O3_3=O3_3.isel(time=timerange)
O3_4=O3_4.isel(time=timerange)
O3_5=O3_5.isel(time=timerange)

O3_c=O3_c*1e6
O3_1=O3_1*1e6
O3_2=O3_2*1e6
O3_3=O3_3*1e6
O3_4=O3_4*1e6
O3_5=O3_5*1e6

fig=plt.figure(1)


plt.plot(O3_c,linewidth='3')
plt.plot(O3_1)
plt.plot(O3_2)
plt.plot(O3_3)
plt.plot(O3_4)
plt.plot(O3_5)


index,xtext=outs.parse_time_axis(ens1.time.isel(time=timerange),10)
plt.xticks(index.tolist(), xtext, size='small')
plt.xlabel('Time'); plt.ylabel('O3 concentration (ppmv)')
plt.title('O3 at 90S 50 hPa')
plt.legend(['cntrl','ens1','ens2','ens3','ens4','ens5'],bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
fig.savefig('files/O3_90S_50hPa_0310-0404.png')