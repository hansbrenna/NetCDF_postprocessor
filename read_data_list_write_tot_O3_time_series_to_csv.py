# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 13:09:41 2016

@author: hanbre

This file reads a file containing a list of 2D (time,lev) O3 NetCDF file paths,
calculates the ozone column in each file and writes all the time series to a 
.csv file.
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

with open(input_file,'r') as file_in:
    c = 0
    for line in file_in:
        l = line.strip('\n')
        c += 1
        ds = xr.open_dataset(l)
        if c == 1:
            length_time=ds.O3.shape[0]
            df = pd.DataFrame(index=np.arange(1,length_time+1))
            
        O3_vmm = ds.O3.squeeze()
            
        
        O3_mmm = O3_vmm*(48.0/28.94)
    
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
        
        O3_t = O3_mmm*(dp.transpose()/g)
        
        O3_tot = O3_t.sum(dim='lev')
        O3_tot_DU = O3_tot/2.1415e-5
        
        df[str(c)]=O3_tot_DU.values
        
        print('hi!')
        
        df.to_csv('{}_O3_time_series.csv'.format(in_name))