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
import HB_module.timing
import HB_module.colordefs

colors = HB_module.colordefs.colordefs()

var = sys.argv[3]

filename1 = sys.argv[1]
filename2 = sys.argv[2]

if 'antarctic' in filename1:
    location1 = 'Antarctic'
    color1 = 'purple'
elif 'arctic' in filename1:
    location1 = 'Arctic'
    color1 = 'green'
elif 'tropics' in filename1:
    location1 = 'Tropics'
    color1 = 'red'
else:
    location1 = 'Global'
    color1 = 'blue'
    
if 'antarctic' in filename2:
    location2 = 'Antarctic'
    color2 = 'purple'
elif 'arctic' in filename2:
    location2 = 'Arctic'
    color2 = 'green'
elif 'tropics' in filename2:
    location2 = 'Tropics'
    color2 = 'red'
else:
    location2 = 'Global'
    color2 = 'blue'

gases = {'BRO':95.9,'CLO':51.45,'O3':48.0,'HCL':36.46,'HBR':80.91}
ranges = {'BRO':(0,8e20),'CLO':(0,1e23),'O3':(100,450),'HCL':(0,2.5e24),'HBR':(0,3.0e20)}

fig = plt.figure()
plt.hold(True)
with open(filename1,'r') as file_in:
    c = 0
    for line in file_in:
        l = line.strip('\n')
        c += 1
        ds = xray.open_dataset(l)
    
        v = getattr(ds,var)        
        O3_vmm = v.squeeze()
            
        
        O3_mmm = O3_vmm*(gases[var]/28.94)
    
        g=9.81
        P0 = ds.P0
        PS = ds.PS
        hyai = ds.hyai
        hyai=hyai[0:len(hyai)-18]
        hybi = ds.hybi
        hybi=hybi[0:len(hybi)-18]
        
    
        if 'new_control' in line:
            O3_mmm=xray.concat([O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm],dim='time')        
            PS = xray.concat([PS,PS,PS,PS,PS,PS,PS,PS,PS,PS],dim='time')
            #P0 = xray.concat([P0,P0,P0,P0,P0],dim='time')
        
        Plevi = hyai*P0+hybi*PS
        Plevi = Plevi.values
        
        dp = np.zeros((O3_mmm.shape[1],120))
        
        for i in xrange(Plevi.shape[1]):
            dp[:,i] = Plevi[1:,i]-Plevi[0:48,i]
        
        O3_t = O3_mmm*(dp.transpose()/g)
        
        O3_tot = O3_t.sum(dim='lev')
        #O3_tot_DU = O3_tot/2.1415e-5
        O3_tot_DU = (1000/gases[var]*6.0221415e23)*O3_tot*1e4 #molecules/cm^2
        
        if c == 1:
            O3_tot_DU_mean = np.zeros((5,len(O3_tot_DU)))

        if 'new_control' in line:
            plt.plot(O3_tot_DU,linewidth='3',label='cntrl',color=colors['darkblue'])
        else:
            O3_tot_DU_mean[c-1,:] = O3_tot_DU        
            plt.plot(O3_tot_DU,linewidth='2',color=colors['pastelblue'],label='ens{0}'.format(c))
        
        if c == 1:
            xtext = ['1-02-01', '2-01-01', '3-01-01', '4-01-01', '5-01-01', '6-01-01', '7-01-01', '8-01-01', '9-01-01', '10-01-01', '11-01-01']
            index=np.array([  0,  11,  23,  35,  47,  59,  71,  83,  95, 107, 119])
            #index, xtext = HB_module.outsourced.parse_time_axis(ds.time,11)
            plt.xticks(index.tolist(),xtext,fontsize='18')
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=45)
    
    plt.ylim(ranges[var])
    locs, labels = plt.yticks()
    plt.setp(labels, fontsize='18')
    plt.plot(np.mean(O3_tot_DU_mean,axis=0),linewidth='3',label='ensm',color=colors['deepblue'])
    locs, labels = plt.yticks()
    plt.setp(labels, fontsize='18')
    plt.xlabel('Time',fontsize='18'); plt.ylabel('Column {0} (molecules/cm^2)'.format(var),fontsize='18')


    
with open(filename2,'r') as file_in:
    c = 0
    for line in file_in:
        l = line.strip('\n')
        c += 1
        ds = xray.open_dataset(l)
    
        v = getattr(ds,var)        
        O3_vmm = v.squeeze()
            
        
        O3_mmm = O3_vmm*(gases[var]/28.94)
    
        g=9.81
        P0 = ds.P0
        PS = ds.PS
        hyai = ds.hyai
        hyai=hyai[0:len(hyai)-18]
        hybi = ds.hybi
        hybi=hybi[0:len(hybi)-18]
        
    
        if 'new_control' in line:
            O3_mmm=xray.concat([O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm,O3_mmm],dim='time')        
            PS = xray.concat([PS,PS,PS,PS,PS,PS,PS,PS,PS,PS],dim='time')
            #P0 = xray.concat([P0,P0,P0,P0,P0],dim='time')
        
        Plevi = hyai*P0+hybi*PS
        Plevi = Plevi.values
        
        dp = np.zeros((O3_mmm.shape[1],120))
        
        for i in xrange(Plevi.shape[1]):
            dp[:,i] = Plevi[1:,i]-Plevi[0:48,i]
        
        O3_t = O3_mmm*(dp.transpose()/g)
        
        O3_tot = O3_t.sum(dim='lev')
        #O3_tot_DU = O3_tot/2.1415e-5
        O3_tot_DU = (1000/gases[var]*6.0221415e23)*O3_tot*1e4 #molecules/cm^2
        
        if c == 1:
            O3_tot_DU_mean = np.zeros((5,len(O3_tot_DU)))

        if 'new_control' in line:
            plt.plot(O3_tot_DU,linewidth='3',label='cntrl',color=colors['darkred'])
        else:
            O3_tot_DU_mean[c-1,:] = O3_tot_DU        
            plt.plot(O3_tot_DU,linewidth='2',color=colors['pastelred'],label='ens{0}'.format(c))
        
        if c == 1:
            xtext = ['1-02-01', '2-01-01', '3-01-01', '4-01-01', '5-01-01', '6-01-01', '7-01-01', '8-01-01', '9-01-01', '10-01-01', '11-01-01']
            index=np.array([  0,  11,  23,  35,  47,  59,  71,  83,  95, 107, 119])
            #index, xtext = HB_module.outsourced.parse_time_axis(ds.time,11)
            plt.xticks(index.tolist(),xtext,fontsize='18')
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=45)
    
    plt.ylim(ranges[var])
    locs, labels = plt.yticks()
    plt.setp(labels, fontsize='18')
    plt.plot(np.mean(O3_tot_DU_mean,axis=0),linewidth='3',label='ensm',color=colors['deepred'])
    locs, labels = plt.yticks()
    plt.setp(labels, fontsize='18')
    plt.xlabel('Time',fontsize='18'); plt.ylabel('Column {0} (molecules/cm^2)'.format(var),fontsize='18')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize='16')
    plt.title('{0} ({1}) and {2} ({3}) column {4}'.format(location1,color1,location2,color2,var),fontsize=18)
    plt.show()
    fig.savefig('files/{0}_{1}_column_{2}.png'.format(location1,location2,var),dpi=200,bbox_inches='tight')
    print('files/{0}_{1}_column_{2}.png was saved'.format(location1,location2,var))
    
