# -*- coding: utf-8 -*-
"""
Created on Tue Feb 09 13:13:49 2016

@author: hanbre

Issues: Implement indexing on lat,lon,lev,time values not index. make sure 
that rest of variables set to mean will be handled correctly with and without 
--index flag set. Implement --anomaly functionality as well as other aesthetic 
functionality from plotter2.py. Implement averaging over ranges and not just 
over entire dimension by giving somehting like --time 1:5 or --time 
0005-02-01:0006-03-01. Implement an optional flag to set the name of the dim
variables so that the program can be used for other data than CAM. 
--dim_names TIME,LEVEL,LAT,LON ( list('TIME,LEVEL,LAT,LON'.split(',')) )
"""
from __future__ import print_function
import argparse
import sys
import os.path
import datetime as dt
import netcdftime
from netcdftime import datetime
import numpy as np
import pandas as pd
import xarray
import scipy
import netCDF4
import matplotlib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import Normalize
import seaborn as sns
import HB_module.outsourced as outs

font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 18}

#rc('font', **font)

matplotlib.rcParams['xtick.labelsize']=16
matplotlib.rcParams['ytick.labelsize']=16
matplotlib.rcParams['ytick.major.pad']=4

class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

def plotter(vm,x,y,norm,cmap,logscale,show):
    #fig=figure()
    print('plotter')
    fig = plt.figure(num=1,figsize=(10,4))
    if xax.name != 'time' and yax.name != 'time':
        xx,yy=np.meshgrid(x,y)
        if xx.shape!=vm.shape:
            vm=vm.transpose()
            
    minimum, maximum, num_cont = outs.check_rangefile(var,vm)
    
    if logscale:
        minimum = np.log10(minimum)
        maximum = np.log10(maximum)
        vm = np.log10(vm)
        
    
    gases = ['O3','HCL','CL','CLY','']
    """Unfortunately the time axis was not properly decoded, so I need to 
    handle plots involving time as axes in a special case"""
    if xax.name != 'time' and yax.name != 'time': 
        
        CF = plt.contourf(x,y,vm,np.linspace(minimum,maximum,num_cont),norm=norm,cmap=cmap)
        CS=plt.contour(x,y,vm,np.linspace(minimum,maximum,num_cont))
    
        try:
            plt.xlabel(x.units);plt.ylabel(y.units)
        except AttributeError:
            plt.xlabel('x'); plt.ylabel('y')
            
        if y.name == 'lev':
            plt.yscale("log")
            plt.ylim(np.amax(y),np.amin(y))
            
    elif xax.name == 'time':
        dummy_x=np.arange(0,len(x))
        CF = plt.contourf(dummy_x,y,vm.transpose(),np.linspace(minimum,maximum,num_cont),norm=norm,cmap=cmap)#norm=matplotlib.colors.LogNorm(vmin=minimum,vmax=maximum),cmap='jet')
        CS = plt.contour(dummy_x,y,vm.transpose(),np.linspace(minimum,maximum,num_cont)) #,norm=matplotlib.colors.LogNorm(),color='k')

        if y.name == 'lev':
            plt.yscale("log")
            plt.ylim(np.amax(y),np.amin(y))

        #plt.axis([0,len(x),len(y),0])
        #plt.yticks(range(0,len(y),13), ['{:E}'.format((y.values[i])) for i in range(0,len(y),13)], fontsize='18')
        if len(x) <= 10:    
            index, xtext = outs.parse_time_axis(x,len(x))
        else:
            index, xtext = outs.parse_time_axis(x,10)
            
        plt.xticks(index.tolist(), xtext, fontsize='18')
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=45)
        plt.ylabel('level (hPa)', fontsize='18')
        #plt.clim(vmin=minimum,vmax=maximum)
        
#        a=np.log10(minimum);b=np.log10(maximum)
#        print(a);print(b)
#        clabs = np.logspace(a,b,num_cont)
#        cticks = np.linspace(a,b,num_cont)
#        print(clabs)
#        
##        for i in range(len(clabs)):
##            if clabs[i]%1:
##                clabs[i]=None
#            
#        print("I'm here 1");print(clabs)
#        clabs = clabs.tolist()
#        print("I'm here 2");print(clabs)
#        c = []
#        for lab in clabs:
#            l = str(lab)
#            l2 = '{0:2g}'.format(lab)
#            c.append(l2)
#        print(c)            
        
#        clb = plt.colorbar(CF,ticks=cticks); clb.set_label('('+v.units+')')
        

#        clb.set_ticklabels(c)
        plt.title('{0} as function of {1} and {2}'.format(var,x.name,y.name),fontsize='18')
    elif yax.name == 'time':
        print('functionality not yet implemented. Use the x-axis for time')
        sys.exit()        
    
    if logscale:
        clb = plt.colorbar(CF); clb.set_label('10^ ('+v.units+')',fontsize='18')
    else:
        clb = plt.colorbar(CF);
        try:
            clb.set_label('('+v.units+')')
        except AttributeError:
            if var == 'T':
                clb.set_label('(K)')
            else:
                clb.set_label(' ')
        #plt.figure(num=1,figsize=(20,10))   
    if show:            
        plt.show()
    title = '{0}_{1}_{2}{3}.png'.format(FileName,var,x.name,y.name)
    fig.savefig(title,bbox_inches='tight')
    print('{0} was saved'.format(title))
    #title=('{0} at {1}={2} and {3}={4}'.format(var,getattr(v,pvar1)[p1],getattr(v,pvar1)[p1].values,getattr(v,pvar2)[p2],getattr(v,pvar2)[p2].values))
    #close(fig)    
    return

desc='''
This program takes the arguments described above and a NetCDF file and 
plots a 2D filled contour plot of the data. The arguments describe what the 
program will do to the data before plotting. All 4 spatio-temporal dimensions
must be given (time, latitude, longitude, level) and the argument tells the 
program how to treat that dimension. The possible values to the dimensional 
arguments are: xax (for assigning x-axis), yax (for y-axis), mean (for telling
the program to average that dimension) and an integer index value for slicing
(--index flag must be given as the slicing on value functionality has not been
implemented yet). Usage example:

python plotter5.py --index -lat xax -lon yax -t mean -lev 35 -v U file/path/name.nc
'''

parser = argparse.ArgumentParser(epilog=desc)
parser.add_argument('FileName')
parser.add_argument('--latitude', '-lat', help='Specify what to do with latidtude', default=None)
parser.add_argument('--longitude', '-lon', help='Specify what to do with longitude', default=None)
parser.add_argument('--time', '-t', help='Specify what to do with time', default=None)
parser.add_argument('--level', '-lev', help='Specify what to do with level', default=None)
parser.add_argument('--Variable', '-v', help='Specify data variable field for plotting', default=None)
parser.add_argument('--anomaly','-a', help='If set, the data are treated as anomalies from a mean state. Divergent color mapping will be applied', action='store_true')
parser.add_argument('--index', '-i', help='Sets the program to index dimension by index. Slicing points should be given as integers', action='store_true')
parser.add_argument('--logarithmic_colors', '-log', help='Sets logarithmic color scaling for the plotted field',action='store_true')
parser.add_argument('--show','-s', help='display plot before saving', action='store_true')

args = parser.parse_args()

show = args.show
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
            

data = xarray.open_dataset(FileName)

#Check that all coordinates in the dataset are accounted for.
for key,value in dims.items():
    try:
        getattr(data,key)
        if dims[key] == None:
            print('{0} is present as a dimension in the dataset. Specify how to handle it at runtime'.format(key))
            sys.exit()
    except AttributeError:
        print('{0} is not present as a dimension in the dataset. Set it to None at runtime')

for key in dims.keys():
    if key not in data.variables and dims[key] != None:
        print(key+' not in dataset. Set the dimension to None at runtime')
        sys.exit()

#assign coordinates to variables for all non-None coordinate axes. 
if dims['lat'] != None:
    lat = data.lat.values
if dims['lon'] != None:
    lon = data.lon.values
if dims['lev'] != None:
    lev = data.lev.values
if dims['time'] != None:
    time = data.time.values

#Check that the specified variable is present in the dataset. Special case for temperature    
if var in data.variables: 
    if var == 'T':
        v = data.variables['T']
    else:
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
        
# Assign the x-axis, y-axis, mean and point axes.
if args.index:
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
else:
    print('Functionality not yet implemented. Please use the --index [-i] flag')
    sys.exit()
        
#Apply normalisation and color map for the plotting function
velocities = ['U','V','OMEGA']
    
if args.anomaly or var in velocities:
    cmap = 'seismic'
    norm = MidpointNormalize(midpoint=0)
else:
    cmap='jet'
    norm = None
    
    
if args.logarithmic_colors:
    logscale = True
else:
    logscale = False
           
print('pointvars ')
print(pointvars)
vm1 = v.mean(dim=meanvars)

vm = vm1[pointvars]

plotter(vm,xax,yax,norm,cmap,logscale,show)


