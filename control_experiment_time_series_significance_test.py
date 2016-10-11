# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 13:53:30 2016

@author: hanbre
"""

from __future__ import print_function
import sys
import argparse
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import HB_module.outsourced
import HB_module.colordefs
from scipy.stats import ttest_ind,ranksums

colors = HB_module.colordefs.colordefs()

desc=""" """

parser = argparse.ArgumentParser(epilog=desc)
parser.add_argument('FileName')
parser.add_argument('--control_region', '-r', help='which region of the globe the control run data is sourced from', default='global')


label_size = 14
matplotlib.rcParams['xtick.labelsize'] = label_size 
matplotlib.rcParams['ytick.labelsize'] = label_size 

args = parser.parse_args()

FileName=args.FileName
fname = FileName.rsplit('.',1)[0]
region = args.control_region

"""Read the control file with each year as one column"""
if region == 'global':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/control_global_control_run.csv',index_col=0)
elif region == 'antarctic':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/control_antarctic_control_run.csv',index_col=0)
elif region == 'arctic':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/control_arctic_control_run.csv',index_col=0)
elif region == 'tropics':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/control_tropics_control_run.csv',index_col=0)

"""Read the experiment file with each experiment time series as one column"""
experiment=pd.read_csv(FileName,index_col=0)


control120=pd.concat([control,control,control,control,control,control,control,control,control,control])
control120.index=np.arange(1,121)
test=pd.DataFrame(index=np.arange(1,121),columns=['statistic','pvalue','r_sum_statistic','r_sum_pvalue'])
for i in experiment.index:
    t=(ttest_ind(control120.loc[i],experiment.loc[i]))
    test['statistic'].loc[i]=t.statistic
    test['pvalue'].loc[i]=t.pvalue
    r=(ranksums(control120.loc[i],experiment.loc[i]))
    test['r_sum_statistic'].loc[i]=r.statistic
    test['r_sum_pvalue'].loc[i]=r.pvalue

fig=plt.figure()
#control120.plot()
std=control120.std(axis=1)
ma = control120.mean(axis=1)
fig=plt.figure()
plt.plot(ma,color=colors['darkblue'],label='control')
plt.hold('on')
plt.fill_between(std.index,ma-2*std, ma+2*std, color=colors['deepblue'], alpha=0.5)
#plt.savefig('tot_glob_O3_natural_variability_m_std.png',dpi=100,bbox_inches='tight')
#plt.hold('on')
#experiment.plot()
std_e = experiment.std(axis=1)
max_e=experiment.max(axis=1)
min_e=experiment.min(axis=1)
me = experiment.mean(axis=1)
plt.plot(me,color=colors['darkred'],label='experiment')
plt.fill_between(std_e.index,me-2*std_e, me+2*std_e, color=colors['deepred'], alpha=0.2)
plt.fill_between(std_e.index,min_e, max_e, color=colors['deepred'], alpha=0.5)
#plt.plot(min_e,color=colors['pastelred'])
#plt.plot(max_e,color=colors['pastelred'])
#plt.setp(labels, fontsize='14')
plt.xlabel('Months since eruption', fontsize='18')
plt.ylabel('Column O3 [DU]', fontsize='18')
plt.xlim((0,35))
plt.title('{}'.format(region),fontsize='18')
fig.savefig('{}_vs_ctr_time_series_with_uncertainty.svg'.format(fname))
print('{}_vs_ctr_time_series_with_uncertainty.svg was saved'.format(fname))

plt.figure()
plt.semilogy(test.index,test.pvalue,test.index,test.r_sum_pvalue,test.index,np.zeros(test.index.shape)+0.05)

plt.show()