# -*- coding: utf-8 -*-
"""
Created on Tue Feb 09 13:13:49 2016

@author: hanbre
"""
from __future__ import print_function
import argparse
import sys
import datetime as dt
import netcdftime
import numpy as np
import pandas as pd
import xray
import scipy
import netCDF4
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import Normalize

class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

def plotter(vm,x,y):
    #fig=figure()
    print('plotter')
    
    xx,yy=np.meshgrid(x,y)
    if xx.shape!=vm.shape:
        vm=vm.transpose()
    
    gases = ['O3','HCL','CL','CLY','']
    if vm.name in gases:
        CF = plt.contourf(x,y,vm,np.linspace(np.amin(vm.values),np.amax(vm.values),10),cmap=matplotlib.cm.jet)
        CS=plt.contour(x, y, vm,np.linspace(np.amin(vm.values),np.amax(vm.values),10),colors='k')
    elif var == 'T':
        CF = plt.contourf(x,y,vm,np.linspace(np.amin(vm.values),400,10),cmap=matplotlib.cm.jet)
        CS=plt.contour(x, y, vm,np.linspace(np.amin(vm.values),400,10),colors='k')
    else:
        norm = MidpointNormalize(midpoint=0)
        CF=plt.contourf(x,y,vm,np.linspace(np.amin(vm.values),np.amax(vm.values),1000),norm=norm,cmap='seismic')
        CS=plt.contour(x, y, vm,10,colors='k')
    try:
        plt.xlabel(x.units);plt.ylabel(y.units)
    except AttributeError:
        plt.xlabel('x'); plt.ylabel('y')
    if y.name == 'lev':
        plt.yscale("log")
    try:
        clb = plt.colorbar(CF); clb.set_label('('+v.units+')')
    except AttributeError:
        clb = plt.colorbar(CF)
    plt.show()
    #title=('{0} at {1}={2} and {3}={4}'.format(var,getattr(v,pvar1)[p1],getattr(v,pvar1)[p1].values,getattr(v,pvar2)[p2],getattr(v,pvar2)[p2].values))
    #close(fig)    
    return

parser = argparse.ArgumentParser()
parser.add_argument('FileName')
parser.add_argument('--latitude', '-lat', help='Specify what to do with latidtude', default='xax')
parser.add_argument('--longitude', '-lon', help='Specify what to do with longitude', default='yax')
parser.add_argument('--time', '-t', help='Specify what to do with time', default='mean')
parser.add_argument('--level', '-lev', help='Specify what to do with level', default='mean')
parser.add_argument('--Variable', '-v', help='Specify data variable field for plotting', default=None)

args = parser.parse_args()

var = args.Variable
assert var != None, 'Variable nedds to be specified by --Variable [-v] variable_name'

    
FileName = args.FileName

dims = {}
dims['lat'] = args.latitude
dims['lon'] = args.longitude
dims['lev'] = args.level
dims['time'] = args.time

for key,value in dims.items():
    if value == 'None':
        dims[key]=None

if 'xax' not in dims.values() or 'yax' not in dims.values():
    print('Both x-axis and y-axis mus be specified')
    print(dims)
    sys.exit()

#==============================================================================
#Parsing NETCDFTIME object from string given to argparser
# try:
#     int(s)
# except ValueError:
#     if s == s.split():
#         print(s)    
#     else:
#         ss = s.split()
#         day = ss[0].split('-')
#         time = ss[1].split(':')

#ts=netcdftime.datetime(05,2,1,0,0,0)
#v.sel(time=ts)
#==============================================================================
            

data = xray.open_dataset(FileName)

for key in dims.keys():
    if key not in data.variables and dims[key] != None:
        print(key+' not in dataset. Set the dimension to None at runtime')
        sys.exit()

if dims['lat'] != None:
    lat = data.lat.values
if dims['lon'] != None:
    lon = data.lon.values
if dims['lev'] != None:
    lev = data.lev.values
if dims['time'] != None:
    time = data.time.values
    
if var in data.variables:   
    v = getattr(data,var)
else:
    print('Variable not in dataset. ')
    print(data.variables.keys())
    sys.exit()

meanvars = []
pointvars = {}

for key,value in dims.items():
    if value == None:
        del(dims[key])
        
print(dims)

for key,value in dims.items():
    if value == None:
        del(dims[key])
    if value == 'xax':        
        xax = getattr(data,key)
    elif value == 'yax':
        yax = getattr(data,key)
    elif value == 'mean':
        meanvars.append(key)
    else:
        if key == 'time':
            pointvars[key] = int(value)
            print('Plotting time: ')
            print(time[pointvars['time']])
        else:
            pointvars[key] = int(value)
            
print('pointvars ')
print(pointvars)
vm1 = v.mean(dim=meanvars)

vm = vm1[pointvars]

plotter(vm,xax,yax)


