# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 12:34:23 2017

@author: hanbre
"""

from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('ticks')
matplotlib.rcParams['xtick.labelsize']=14
matplotlib.rcParams['ytick.labelsize']=14

def calculate_total_ozone(ds):
    #ds
    #ds.O3
    O3_vmm = ds.O3
    O3_mmm = O3_vmm*(48.0/28.94)
    
    g=9.81
    P0 = ds.P0
    PS = ds.PS
    hyai = ds.hyai
    hybi = ds.hybi
    Plevi = hyai*P0+hybi*PS
    
    dp = np.empty(shape=O3_vmm.shape)
    
    dpa=xr.DataArray(dp,coords=ds.O3.coords,dims=ds.O3.dims)
    
    for i in range(1,Plevi.shape[0]):
        dpa[dict(lev=i-1)]=Plevi[i]-Plevi[i-1]
        
    O3_t=O3_mmm*dpa/g
    
    totO3=O3_t.sum(dim='lev')
    
    totO3DU = totO3/2.1415e-5
    
    ds2=totO3DU.to_dataset(name='totO3')
    ds3=ds.merge(ds2)
    ds3.totO3.attrs['units']='DU'
    ds3.totO3.attrs['long_name']='Column ozone in Dobson Units'
    return ds3
    
def find_minimum(data): 
    """Give xarray.DataArray as input"""
    min_data = data.min(dim=['lat','lon'])
    min_series = min_data.to_series()
    return min_series
    
input_file = sys.argv[1]
in_name = input_file.split('.')[0]
min_tot_O3 = []
with open(input_file,'r') as file_in:
    c = 0
    for line in file_in:
        l = line.strip('\n')
        c += 1
        ds = xr.open_dataset(l,decode_times=False)
        ds3 = calculate_total_ozone(ds)
        min_tot_O3_temp = find_minimum(ds3.totO3)
        min_tot_O3.append(min_tot_O3_temp.values)

min_tot_O3_array = np.array(min_tot_O3).transpose()
dummy_time = np.arange(1,len(min_tot_O3_temp)+1)
minimums = pd.DataFrame(min_tot_O3_array,index=dummy_time)
minimums.to_csv('{}_time_series.csv'.format(in_name))
list_min = np.array_split(minimums,12)
list_yearly_mins = []
for element in list_min:
    temp = element.min()
    element = element.where(element == temp)
    list_yearly_mins.append(element)
    
masked_df = pd.DataFrame()
for e in list_yearly_mins:
    masked_df=masked_df.append(e)
    
fig = plt.figure(figsize=(10,5))
plt.plot(masked_df,'o')
text = ['J','A','J','O']
locs = np.arange(1,145,3)
labels = 12*text
plt.xlim(1,144)
plt.xticks(locs,labels)
plt.legend(['full.1','full.2','full.3','full.4','full.5'],loc='lower right',fontsize=14)
plt.xlabel('Month',fontsize=16)
plt.ylabel('Column O3 [DU]',fontsize=16)
fig.savefig('full_yearly_antarctic_minimum_totO3.png',figsize=(10,4),dpi=300,bbox_inches='tight')
plt.show()

