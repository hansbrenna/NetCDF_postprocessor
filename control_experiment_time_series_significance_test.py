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

def parse_comma_separated_list(text):
    text_list = text.split(',')
    int_list = [int(element) for element in text_list]
    return int_list

def extract_months(data,months):
    months_array = np.array(months)
    data_months = []
    while max(months_array)<max(data.index):
        data_months.append(months_array)
        months_array = months_array+12
    data_months = np.array(data_months)
    data_months = data_months.reshape([1,data_months.size])
    data_months = data_months.squeeze()
    extr_data = data.loc[data_months]
    return extr_data
        
        

colors = HB_module.colordefs.colordefs()

sns.set_style('ticks')

desc=""" """

parser = argparse.ArgumentParser(epilog=desc)
parser.add_argument('FileName')
parser.add_argument('--control_region', '-r', help='which region of the globe the control run data is sourced from', default='global')
parser.add_argument('--variable','-v',help='sepcify which variable',default='O3')
parser.add_argument('--noSave','-ns',help="don't save the output figures or show them, useful when plotting more than one series in the same axis. Also turns of significance testing",action='store_true')
parser.add_argument('--experiment_color','-ec',help='set the color for the experiment time series (names from HB_module.colordefs',default='red')
parser.add_argument('--exp_label','-el',help='set the experiment label text')
parser.add_argument('--extract_months','-em',help="extract certain months. Give numbers as comma separated list (jan=1). Example: 1,2,9,10,11,12",default=False)
parser.add_argument('--significance_test','-test',help='toggle on statistical significance testing',action='store_true')

label_size = 14
matplotlib.rcParams['xtick.labelsize'] = label_size 
matplotlib.rcParams['ytick.labelsize'] = label_size 

args = parser.parse_args()

FileName=args.FileName
fname = FileName.rsplit('.',1)[0]
region = args.control_region
var = args.variable
if args.extract_months != False:
    months = parse_comma_separated_list(args.extract_months)

"""Read the control file with each year as one column"""
if region == 'global':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/global_{}_control_run.csv'.format(var),index_col=0)
elif region == 'antarctic':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/antarctic_{}_control_run.csv'.format(var),index_col=0)
elif region == 'arctic':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/control_arctic_control_run.csv',index_col=0)
elif region == '65N':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/65N_O3_control_run.csv',index_col=0)
elif region == '65S':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/65S_O3_control_run.csv',index_col=0)
elif region == '70S':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/70S_O3_control_run.csv',index_col=0)
elif region == '75S':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/75S_O3_control_run.csv',index_col=0)
elif region == 'tropics':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/control_tropics_control_run.csv',index_col=0)
elif region == 'nh_extratropics':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/control_nh_extratropics_control_run.csv',index_col=0)
elif region == 'sh_extratropics':
    control=pd.read_csv('/home/hanbre/norstore_project/BCKUP_after_21.07.15/new_control_test/time_series/control_sh_extratropics_control_run.csv',index_col=0)
elif region == 'None':
    control = None
else:
    print('region not recognised. see documentation')
    sys.exit()

"""Read the experiment file with each experiment time series as one column"""
experiment=pd.read_csv(FileName,index_col=0)
if args.extract_months != False:
    experiment = extract_months(experiment,months)
    


if region != 'None':
    #fig=plt.figure()
    control120=pd.concat([control,control,control,control,control,control,control,control,control,control,control,control])
    control120.index=np.arange(1,control120.shape[0]+1)
    if args.extract_months != False:
        control120 = extract_months(control120,months)
    test=pd.DataFrame(index=np.arange(1,control120.shape[0]+1),columns=['statistic','pvalue','r_sum_statistic','r_sum_pvalue'])
    for i in experiment.index:
        t=(ttest_ind(control120.loc[i],experiment.loc[i]))
        test['statistic'].loc[i]=t.statistic
        test['pvalue'].loc[i]=t.pvalue
        r=(ranksums(control120.loc[i],experiment.loc[i]))
        test['r_sum_statistic'].loc[i]=r.statistic
        test['r_sum_pvalue'].loc[i]=r.pvalue
    std=control120.std(axis=1)
    ma = control120.mean(axis=1)
    if args.extract_months == False:
        plt.plot(ma,color=colors['darkblue'],label='ctr')
        plt.fill_between(std.index,ma-2*std, ma+2*std, color=colors['deepblue'], alpha=0.5)
    else:
        dummy_t = np.arange(1,len(control120.index)+1)
        plt.plot(dummy_t,ma,color=colors['darkblue'],label='ctr')
        plt.fill_between(dummy_t,ma-2*std, ma+2*std, color=colors['deepblue'], alpha=0.5)
#control120.plot()


plt.hold('on')

#plt.savefig('tot_glob_O3_natural_variability_m_std.png',dpi=100,bbox_inches='tight')
#plt.hold('on')
#experiment.plot()
std_e = experiment.std(axis=1)
max_e=experiment.max(axis=1)
min_e=experiment.min(axis=1)
me = experiment.mean(axis=1)
if args.extract_months == False:
    plt.plot(me,color=colors['dark{}'.format(args.experiment_color)],label=args.exp_label)
    plt.fill_between(std_e.index,me-2*std_e, me+2*std_e, color=colors['deep{}'.format(args.experiment_color)], alpha=0.5)
else:
    dummy_t = np.arange(1,len(experiment.index)+1)
    plt.plot(dummy_t,me,color=colors['dark{}'.format(args.experiment_color)],label=args.exp_label)
    plt.fill_between(dummy_t,me-2*std_e, me+2*std_e, color=colors['deep{}'.format(args.experiment_color)], alpha=0.5)
#plt.fill_between(std_e.index,min_e, max_e, color=colors['deepred'], alpha=0.5)
#plt.plot(min_e,color=colors['pastelred'])
#plt.plot(max_e,color=colors['pastelred'])
#plt.setp(labels, fontsize='14')
plt.xlabel('Months since eruption', fontsize='18')
plt.ylabel('Column O3 [DU]', fontsize='18')
#plt.xlim((0,35))
if region != 'None':
    plt.title('{}'.format(region),fontsize='18')

if args.noSave == False:
    plt.legend(fontsize=14,loc='lower right')
    plt.savefig('{}_vs_ctr_time_series_with_uncertainty.svg'.format(fname),bbox_inches='tight')
    print('{}_vs_ctr_time_series_with_uncertainty.svg was saved'.format(fname))
#    plt.figure()
    plt.semilogy(test.index,test.pvalue,test.index,test.r_sum_pvalue,test.index,np.zeros(test.index.shape)+0.05)
    #plt.show()
