# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 13:09:41 2016

@author: hanbre

This file reads a file containing a list of 2D (time,lev) O3 NetCDF file paths,
calculates the ozone column in each file and writes all the time series to a 
.csv file.

/foo/bar/file1.nc
/foo/bar/file2.nc
...
"""

from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import HB_module.outsourced
import HB_module.colordefs

#df = pd.DataFrame(index=np.arange(1,121))

input_file = sys.argv[1]
in_name = input_file.split('.')[0]
var = sys.argv[2]
gases = {'BRO':95.9,'CLO':51.45,'O3':48.0,'HCL':36.46,'HBR':80.91}
T = ['']
with open(input_file,'r') as file_in:
    c = 0
    for line in file_in:
        l = line.strip('\n')
        c += 1
        ds = xr.open_dataset(l)
        
        if c == 1:
            length_time=ds[var].shape[0]
            df = pd.DataFrame(index=np.arange(1,length_time+1))
            
        O3_vmm = ds[var].squeeze()
        
        if var in gases.keys() or var in T:        
            g=9.81
            P0 = ds.P0
            PS = ds.PS
            hyai = ds.hyai
            hybi = ds.hybi
            
            Plevi = hyai*P0+hybi*PS
            Plevi = Plevi.values
            
            dp = np.zeros((66,length_time))
            
            for i in xrange(Plevi.shape[1]):
                dp[:,i] = Plevi[1:,i]-Plevi[0:66,i]
            
            if var in gases.keys():
                O3_mmm = O3_vmm*(gases[var]/28.94)
                O3_t = O3_mmm*(dp.transpose()/g)            
                O3_tot = O3_t.sum(dim='lev')
                O3_tot_DU = O3_tot/2.1415e-5
            elif var in T:
                T = O3_vmm
                M =(dp.transpose()/g)
                TM = T*M
                Tmean = np.average(TM.values, axis = 1, weights = M)
                TM.values = Tmean
                O3_tot_DU = TM
            
            df[str(c)]=O3_tot_DU.values
        else:
            df[str(c)]=O3_vmm.values
            
        print('hi!')
        
        df.to_csv('{}_time_series.csv'.format(in_name))