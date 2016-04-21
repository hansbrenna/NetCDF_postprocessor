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

sns.set_palette('deep')
fig = plt.figure()
plt.hold(True)

deepblue = (0.2980392156862745, 0.4470588235294118, 0.6901960784313725)
pastelblue = (0.5725490196078431, 0.7764705882352941, 1.0)
darkblue = (0.0, 0.10980392156862745, 0.4980392156862745)
deepgreen = (0.3333333333333333, 0.6588235294117647, 0.40784313725490196)
darkgreen = (0.00392156862745098, 0.4588235294117647, 0.09019607843137255)
pastelgreen = (0.592156862745098, 0.9411764705882353, 0.6666666666666666)
pastelred = (1.0, 0.6235294117647059, 0.6039215686274509)
deepred = (0.7686274509803922, 0.3058823529411765, 0.3215686274509804)
darkred = (0.5490196078431373, 0.03529411764705882, 0.0)
pastelpurple = (0.8156862745098039, 0.7333333333333333, 1.0)
darkpurple = (0.4627450980392157, 0.0, 0.6313725490196078)
deeppurple = (0.5058823529411764, 0.4470588235294118, 0.6980392156862745)

with open('files/tot_O3_arctic_list.dat','r') as file_in:
    c = 0
    #sns.set_palette('dark')
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
        Plevi = Plevi.values
        
        dp = np.zeros((66,120))
        
        for i in xrange(Plevi.shape[1]):
            dp[:,i] = Plevi[1:,i]-Plevi[0:66,i]
        
        O3_t = O3_mmm*(dp.transpose()/g)
        
        O3_tot = O3_t.sum(dim='lev')
        O3_tot_DU = O3_tot/2.1415e-5
        
        if c == 1:
            O3_tot_DU_mean = np.zeros((5,len(O3_tot_DU)))

        if 'new_control' in line:
            plt.plot(O3_tot_DU,linewidth='3',label='cntrl',color=darkblue)
        else:
            O3_tot_DU_mean[c-1,:] = O3_tot_DU        
            plt.plot(O3_tot_DU,linewidth='2',color=pastelblue,label='ens{0}'.format(c))
        
        if c == 1:
            index, xtext = HB_module.outsourced.parse_time_axis(ds.time,11)
            plt.xticks(index.tolist(),xtext,fontsize='18')
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=45)
    
    
    locs, labels = plt.yticks()
    plt.setp(labels, fontsize='18')
    plt.ylim(100,450)
    plt.plot(np.mean(O3_tot_DU_mean,axis=0),linewidth='3',label='ensm',color=deepblue)
    plt.xlabel('Time',fontsize='18'); plt.ylabel('Column O3 (DU)',fontsize=18)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize='16')
    #plt.title('Arctic column ozone',fontsize=18)
   #plt.show()
    #fig.savefig('files/tot_ant-arctic_O3.png',dpi=200,bbox_inches='tight')
    
with open('files/tot_O3_antarctic_list.dat','r') as file_in:
    c = 0
    #sns.set_palette('dark')
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
        Plevi = Plevi.values
        
        dp = np.zeros((66,120))
        
        for i in xrange(Plevi.shape[1]):
            dp[:,i] = Plevi[1:,i]-Plevi[0:66,i]
        
        O3_t = O3_mmm*(dp.transpose()/g)
        
        O3_tot = O3_t.sum(dim='lev')
        O3_tot_DU = O3_tot/2.1415e-5
        
        if c == 1:
            O3_tot_DU_mean = np.zeros((5,len(O3_tot_DU)))

        if 'new_control' in line:
            plt.plot(O3_tot_DU,linewidth='3',label='cntrl',color=darkred)
        else:
            O3_tot_DU_mean[c-1,:] = O3_tot_DU        
            plt.plot(O3_tot_DU,linewidth='2',color=pastelred,label='ens{0}'.format(c))
        
        if c == 1:
            index, xtext = HB_module.outsourced.parse_time_axis(ds.time,11)
            plt.xticks(index.tolist(),xtext,fontsize='18')
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=45)
    
    
    locs, labels = plt.yticks()
    plt.setp(labels, fontsize='18')
    plt.ylim(100,450)
    plt.plot(np.mean(O3_tot_DU_mean,axis=0),linewidth='3',label='ensm',color=deepred)
    plt.xlabel('Time',fontsize='18'); plt.ylabel('Column O3 (DU)',fontsize=18)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize='16')
    plt.title('Global (blue) and Tropics (red) column ozone',fontsize=18)
    #plt.show()
    #fig.savefig('files/tot_glob-trops_O3.png',dpi=200,bbox_inches='tight')