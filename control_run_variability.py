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
    
        O3_vmm = ds.O3.squeeze()
            
        
        O3_mmm = O3_vmm*(48.0/28.94)
    
        g=9.81
        P0 = ds.P0
        PS = ds.PS
        hyai = ds.hyai
        hybi = ds.hybi
    
#        if 'new_control' in line:
#            O3_mmm=xray.concat([O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm],dim='time')        
#            PS = xray.concat([PS,PS,PS,PS,PS,PS,PS,PS,PS,PS],dim='time')
#            #P0 = xray.concat([P0,P0,P0,P0,P0],dim='time')
        
        Plevi = hyai*P0+hybi*PS
        Plevi = Plevi.values
        
        dp = np.zeros((66,12))
        
        for i in xrange(Plevi.shape[1]):
            dp[:,i] = Plevi[1:,i]-Plevi[0:66,i]
        
        O3_t = O3_mmm*(dp.transpose()/g)
        
        O3_tot = O3_t.sum(dim='lev')
        O3_tot_DU = O3_tot/2.1415e-5
        
#        if c == 1:
#            O3_tot_DU_mean = np.zeros((5,len(O3_tot_DU)))
        
        df[str(c)]=O3_tot_DU.values


#        if 'new_control' in line:
#            plt.plot(O3_tot_DU,linewidth='3',label='cntrl',color=darkblue)
#        else:
#            O3_tot_DU_mean[c-1,:] = O3_tot_DU        
#            plt.plot(O3_tot_DU,linewidth='2',color=pastelblue,label='ens{0}'.format(c))
        
#        if c == 1:
#            index, xtext = HB_module.outsourced.parse_time_axis(ds.time,11)
#            plt.xticks(index.tolist(),xtext,fontsize='18')
#            locs, labels = plt.xticks()
#            plt.setp(labels, rotation=45)
    
#    
#    locs, labels = plt.yticks()
#    plt.setp(labels, fontsize='18')
#    plt.ylim(100,450)
#    plt.plot(np.mean(O3_tot_DU_mean,axis=0),linewidth='3',label='ensm',color=deepblue)
    df.plot(colormap='winter',figsize=(10,10))
    std=df.std(axis=1)
    ma = df.mean(axis=1)
    plt.xlabel('Month',fontsize='18'); plt.ylabel('Column O3 (DU)',fontsize=18)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize='14')
    #plt.title('Arctic column ozone',fontsize=18)
#    plt.show()
    plt.savefig('{}_O3_natural_variability.svg'.format(in_name),dpi=100,bbox_inches='tight')
    plt.savefig('{}_O3_natural_variability.png'.format(in_name),dpi=100,bbox_inches='tight')    
    
    fig=plt.figure()
    plt.plot(ma,color=colors['darkblue'])
    plt.hold('on')
    plt.fill_between(std.index,ma-2*std, ma+2*std, color=colors['deepblue'], alpha=0.2)
    plt.savefig('{}_O3_m_std.svg'.format(in_name),dpi=100,bbox_inches='tight')
    plt.savefig('{}_O3_m_std.png'.format(in_name),dpi=100,bbox_inches='tight')
    
    fig3=plt.figure()
    #Deseasonalise
    df_ds = df.sub(ma,axis=0)
    df_ds_s=df_ds.stack()
    sns.distplot(df_ds_s)
    #plt.show()
    plt.savefig('{}_O3_kde.svg'.format(in_name),dpi=100,bbox_inches='tight')
    plt.savefig('{}_O3_kde.png'.format(in_name),dpi=100,bbox_inches='tight')
    
    fig4=plt.figure()
    df_ds_s.hist(bins=19)
    plt.savefig('{}_O3_histogram.svg'.format(in_name),dpi=100,bbox_inches='tight')
    plt.savefig('{}_O3_histogram.png'.format(in_name),dpi=100,bbox_inches='tight')
    
    df.to_csv('{0}_control_run.csv'.format(in_name))
    
    plt.close('all')
    