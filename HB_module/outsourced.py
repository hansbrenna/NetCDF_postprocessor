# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:46:10 2016

@author: hanbre
"""
import os.path
import numpy as np
import pandas as pd
import xray

def parse_time_axis(t,res):
    #"""parse_time_axis(time_axis, resolution) parses an xray DataArray of netcdftime objects into a list of strings to be used for axis labelling"""
    print(t)
    length = t.shape[0]
    print(length)
    ind = np.floor(np.linspace(0,length-1,res)).astype(int)
    print(ind)
    xtemp = str(t.values[ind].tolist()).strip('[').strip(']').split(',')
    text = [i.split()[0] for i in xtemp]
    print(text)
    return ind, text    

def check_rangefile(var,vm): 
    print('\n Cheking for rangefile for plotting ranges.dat in current dir...\n')            
    if os.path.isfile('ranges.dat'):
        print('Rangefile found, using ranges.dat')
        with open('ranges.dat') as rangefile:
            header = next(rangefile)
            ranges = {}
            for line in rangefile:
                l=line.strip('\n').split(' ')
                key=l[0]
                rge = [l[1],l[2],l[3]]
                ranges[key]=rge
    else:
        print('Rangefile not found using min and max of field as ranges')
        ranges = {}
            
    if var in ranges.keys():
        print('Current variable in rangefile')
        minimum = float(ranges[var][0]); maximum=float(ranges[var][1])
        num_cont = int(ranges[var][2])
    else:
        print('Current variable not found in rangefile, using default ranges')
        minimum = np.amin(vm.values); maximum = np.amax(vm.values); num_cont = 16
    return minimum, maximum, num_cont