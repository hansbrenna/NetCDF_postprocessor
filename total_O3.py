# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:35:44 2016

@author: hanbre
"""
from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import xray
import matplotlib.pyplot as plt
import seaborn as sns
import HB_module.outsourced

with open('files/tot_O3_file_list2.dat','r') as file_in:
    fig = plt.figure()
    c = 0
    sns.set_palette('dark')
    for line in file_in:
        l = line.strip('\n')
        c += 1
        ds = xray.open_dataset(l)
    
        O3_vmm = ds.O3.squeeze()
            
        
        O3_mmm = O3_vmm*(48.0/28.94)
    
        g=9.81
        P0 = ds.P0
        PS = ds.PS
        hyai = ds.hyai
        hybi = ds.hybi
    
        if 'new_control' in line:
            O3_mmm=xray.concat([O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm],dim='time')        
            PS = xray.concat([PS,PS,PS,PS,PS,PS,PS,PS,PS,PS],dim='time')
            #P0 = xray.concat([P0,P0,P0,P0,P0],dim='time')
        
        Plevi = hyai*P0+hybi*PS
        
        dp = np.zeros((66,120))
        
        for i in range(Plevi.shape[1]):
            dp[:,i] = [Plevi[j,i]-Plevi[j-1,i] for j in range(1,Plevi.shape[0])]
        
        O3_t = O3_mmm*(dp.transpose()/g)
        
        O3_tot = O3_t.sum(dim='lev')
        O3_tot_DU = O3_tot/2.1415e-5
        
        if c == 1:
            O3_tot_DU_mean = np.zeros((5,len(O3_tot_DU)))

        if 'new_control' in line:
            plt.plot(O3_tot_DU,linewidth='3',label='cntrl',color='k')
        else:
            O3_tot_DU_mean[c-1,:] = O3_tot_DU        
            plt.plot(O3_tot_DU,label='ens{0}'.format(c),linewidth='2')
        
        if c == 1:
            index, xtext = HB_module.outsourced.parse_time_axis(ds.time,11)
            plt.xticks(index.tolist(),xtext,fontsize='18')
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=45)
    
    sns.set_palette('deep')
    plt.plot(np.mean(O3_tot_DU_mean,axis=0),linewidth='3',label='ensm',color='c')
    plt.xlabel('Time',fontsize='18'); plt.ylabel('Column O3 (DU)',fontsize=18)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize='16')
    plt.title('Global column ozone',fontsize=18)
    plt.show()
    fig.savefig('files/tot_O3.png',dpi=200,bbox_inches='tight')