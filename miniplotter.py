# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 13:54:44 2016

@author: hanbre
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xray
import seaborn as sns

ds = xray.open_dataset('files/f1850w.new_control.cam.h5.0001-0030.10hpa.zon.TU.nc')

#Plot U10 60N

U60 = ds.U[dict(lat=79)]
time = np.arange(1,366,0.5)

#Plot all in one file

for i in range(1,31):
    plt.plot(time,U60[(i*730-730):i*730])
    plt.axis([0,366,-100,100])
    
plt.savefig('files/all_30_years_U60.png',dpi=200)

#Plot 5 in one file
plt.figure()

for i in range(1,31):
    plt.plot(time,U60[(i*730-730):i*730])
    plt.axis([0,366,-100,100])
    if i%5==0:
        plt.savefig('files/{0}_U60.png'.format(i),dpi=200)
        plt.figure()

#Plot mean over all years
plt.figure()

U = []
for i in range(1,31):
    U.append(U60[(i*730-730):i*730].values)
    
Ua=np.array(U)
Um=np.mean(Ua,axis=0)

plt.plot(time,Um)
plt.savefig('files/mean_U60.png',dpi=200)

#Plot U10 60S
U_60 = ds.U[dict(lat=16)]

#Plot all in one file
plt.figure()

for i in range(1,31):
    plt.plot(time,U_60[(i*730-730):i*730])
    plt.axis([0,366,-100,100])
    U
    
plt.savefig('files/all_30_years_U-60.png',dpi=200)
    
#Plot 5 in one file    

plt.figure()

for i in range(1,31):
    plt.plot(time,U_60[(i*730-730):i*730])
    plt.axis([0,366,-100,100])
    if i%5==0:
        plt.savefig('files/{0}_U-60.png'.format(i),dpi=200)
        plt.figure()

#Plot mean of all years
plt.figure() 
   
U = []
for i in range(1,31):
    U.append(U_60[(i*730-730):i*730].values)
    
Ua=np.array(U)
Um=np.mean(Ua,axis=0)

plt.plot(time,Um)
plt.savefig('files/mean_U-60.png',dpi=200)