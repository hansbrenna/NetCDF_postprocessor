# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:46:10 2016

@author: hanbre
"""
import os.path
import sys
import numpy as np
import pandas as pd
import xarray
import re

def parse_time_axis(t,res,verbose=True):
    #"""parse_time_axis(time_axis, resolution) parses an xray DataArray of netcdftime objects into a list of strings to be used for axis labelling"""
    #print(t)
    length = t.shape[0]
    ind = np.floor(np.linspace(0,length-1,res)).astype(int)
    xtemp = str(t.values[ind].tolist()).strip('[').strip(']').split(',')
    text = [i.split()[0] for i in xtemp]    
    if verbose:
        print(length)
        print(ind)
        print(text)
        
    return ind, text    

def check_rangefile(ranges,var,vm): 
    print('\n Cheking for rangefile {0} in current dir...\n'.format(ranges))            
    if os.path.isfile(ranges):
        print('Rangefile found, using {0}'.format(ranges))
        with open(ranges) as rangefile:
            header = next(rangefile)
            if 'num_cont' in header:
                print('range file found in mode (min max num)')
                ranges = {}
                for line in rangefile:
                    l=line.strip('\n').split(' ')
                    key=l[0]
                    rge = [l[1],l[2],l[3]]
                    ranges[key]=rge
                if var in ranges.keys():
                    print('Current variable in rangefile')
                    minimum = float(ranges[var][0]); maximum=float(ranges[var][1])
                    num_cont = int(ranges[var][2])
                    clevels = np.linspace(minimum,maximum,num_cont)
                else:
                    print('Current variable not found in rangefile, using default ranges')
                    minimum = np.amin(vm.values); maximum = np.amax(vm.values); num_cont = 16
                    clevels = np.linspace(minimum,maximum,num_cont)
            elif 'levels' in header:
                print('rangefile found in mode (clevels)')
                ranges = {}
                for line in rangefile:
                    l=line.strip('\n').split(' ')
                    key = l[0]
                    l.remove(key)
                    levels = np.array(l).astype(float)
                    ranges[key]=levels
                if var in ranges.keys():
                    print('Current variable in rangefile')
                    clevels = ranges[var]
                else:
                    print('Current variable not found in rangefile, using default ranges')
                    minimum = np.amin(vm.values); maximum = np.amax(vm.values); num_cont = 16
                    clevels = np.linspace(minimum,maximum,num_cont)
            else:
                print('something went wrong with the ranges. Check the range file')
                sys.exit()
    else:
        print('Rangefile not found using min and max of field as ranges')
        ranges = {}
        minimum = np.amin(vm.values); maximum = np.amax(vm.values); num_cont = 16
        clevels = np.linspace(minimum,maximum,num_cont)
    return clevels
    
def make_labels(var,vm,x,y):
    try:
        if x.name == 'lat':
            xl = 'Latitude'
        elif x.name == 'lon':
            xl = 'Longitude'
        elif x.name == 'lev':
            xl = 'Level (hPa)'
        elif x.name == 'time':
            xl = 'Time'
        if y.name == 'lat':
            yl = 'Latitude'
        elif y.name == 'lon':
            yl = 'Longitude'
        elif y.name == 'lev':
            yl = 'Level (hPa)'
        elif y.name == 'time':
            yl = 'Time'
    except AttributeError:
        print('WARNING: No such attribute to x or y. Using default labels')
        xl='x'; yl='y'
        
    return xl, yl    

def make_timestamp(SearchString):
    pattern = re.compile('[0-9]{4}-[0-9]{2}')
    sub = pattern.search(SearchString)
    timestamp = sub.group()
    #title('Variable: '+var+'    Time: '+timestamp)
    return timestamp
    
def make_timestamp_clim(SearchString):
    pattern = re.compile('h0.[0-9]{2}.')
    sub = pattern.search(SearchString)
    timestamp = sub.group()
    #title('Variable: '+var+'    Time: '+timestamp)
    return timestamp

def clb_labels(var,ppm,ppb,ppt):       
    if var in ppt:
        cl = ' {0} (pptv)'.format(var)
    elif var in ppb:
        cl = ' {0} (ppbv)'.format(var)
    elif var in ppm:
        cl = ' {0} (ppmv)'.format(var)
    elif var == 'T':
        cl = 'Temperature (C)'
    elif var == 'U':
        cl='Zonal wind (m/s)'
    elif var == 'V':
        cl='Meridional wind (m/s)'
    elif var == 'OMEGA':
        cl='Vertical wind (Pa/s)'
    elif var == 'O3_CHML':
        cl = 'O3 chmical loss rate (/cm3/s)'
    elif var == 'O3_CHMP':
        cl = 'O3 chmical production rate (/cm3/s)'
    elif var == 'QRS':
        cl = 'Short wave heating rate (K/s)'
    elif var == 'QRL':
        cl = 'Long wave heating rate (K/s)'
    else:
        cl = '{}'.format(var)
    return cl
    #clabel(CS,inline=1,fontsize=8)
    
def gaussian_weights():
    data = xarray.open_dataset('/home/hanbre/uio_home/GitHub/NetCDF_postprocessor/HB_module/gw.nc')
    gw = data['gw']
    return gw
