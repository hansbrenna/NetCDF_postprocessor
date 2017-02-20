# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 11:12:51 2016

@author: hanbre

This program takes an input-file which lists netcdf files containing horizonta-
lly averaged O3 concentrations in 67 WACCM layers and calculates total O3. 
Each file is treated as a single year of a control simulations and the program
characterizes the natural interannual variability in the run. It also saves the
individual yearly time series as columns in a .csv file for further processing
or ease of reuse. as long as the files contains a single horizontal grid point
this program is applicable.
"""
from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import HB_module.outsourced
import HB_module.colordefs

label_size = 14
matplotlib.rcParams['xtick.labelsize'] = label_size 
matplotlib.rcParams['ytick.labelsize'] = label_size 

colors = HB_module.colordefs.colordefs()
input_file = sys.argv[1]
var = sys.argv[2]
gases = {'BRO':95.9,'CLO':51.45,'O3':48.0,'HCL':36.46,'HBR':80.91}
T = ['']
ppt = ['BRO','BROY','HBR']        
ppb = ['CLOY','CLO','HCL']
ppm = ['O3']
region = 'global'
in_name = input_file.split('.')[0]
df = pd.DataFrame(index=np.arange(1,13))
#fig = plt.figure(figsize=(20,20))
with open(input_file,'r') as file_in:
    c = 4
    #sns.set_palette('dark')
    for line in file_in:
        l = line.strip('\n')
        c += 1
        ds = xr.open_dataset(l)
    
        O3_vmm = ds[var].squeeze()
        if var in gases.keys() or var in T:        
            g=9.81
            P0 = ds.P0
            PS = ds.PS
            hyai = ds.hyai
            hybi = ds.hybi
            
            Plevi = hyai*P0+hybi*PS
            Plevi = Plevi.values
            
            dp = np.zeros((66,12))
            
            for i in xrange(Plevi.shape[1]):
                dp[:,i] = Plevi[1:,i]-Plevi[0:66,i]
            
            if var in gases.keys():
                O3_mmm = O3_vmm*(gases[var]/28.94)
                O3_t = O3_mmm*(dp.transpose()/g)            
                O3_tot = O3_t.sum(dim='lev')
                O3_tot_DU = O3_tot/2.1415e-5
            elif var in T:
                T = O3_vmm
                M =(dp[0:len(T.lev)].transpose()/g)
                TM = T*M
                Tmean = np.average(TM.values, axis = 1, weights = M)
                TM.values = Tmean
                O3_tot_DU = TM
            
            df[str(c)]=O3_tot_DU.values
        else:
            df[str(c)]=O3_vmm.values

    df.plot(colormap='winter',figsize=(10,10))
    std=df.std(axis=1)
    ma = df.mean(axis=1)
    #yl = HB_module.outsourced.clb_labels(var)
    plt.xlabel('Month',fontsize='18'); plt.ylabel('Column {} (DU)'.format(var),fontsize=18)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize='14')
    #plt.title('Arctic column ozone',fontsize=18)
#    plt.show()
    plt.savefig('{}_{}_natural_variability.svg'.format(in_name,var),dpi=100,bbox_inches='tight')
    plt.savefig('{}_{}_natural_variability.png'.format(in_name,var),dpi=100,bbox_inches='tight')    
    
    fig=plt.figure()
    plt.plot(ma,color=colors['darkblue'])
    plt.hold('on')
    plt.fill_between(std.index,ma-2*std, ma+2*std, color=colors['deepblue'], alpha=0.2)
    plt.savefig('{}_{}_m_std.svg'.format(in_name,var),dpi=100,bbox_inches='tight')
    plt.savefig('{}_{}_m_std.png'.format(in_name,var),dpi=100,bbox_inches='tight')
    
    fig3=plt.figure()
    #Deseasonalise
    df_ds = df.sub(ma,axis=0)
    df_ds_s=df_ds.stack()
    sns.distplot(df_ds_s)
    #plt.show()
    plt.savefig('{}_{}_kde.svg'.format(in_name,var),dpi=100,bbox_inches='tight')
    plt.savefig('{}_{}_kde.png'.format(in_name,var),dpi=100,bbox_inches='tight')
    
    fig4=plt.figure()
    df_ds_s.hist(bins=19)
    plt.savefig('{}_{}_histogram.svg'.format(in_name,var),dpi=100,bbox_inches='tight')
    plt.savefig('{}_{}_histogram.png'.format(in_name,var),dpi=100,bbox_inches='tight')
    
    df.to_csv('{}_{}_control_run.csv'.format(region,var))
    
    plt.close('all')
    