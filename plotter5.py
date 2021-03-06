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
import re
import seaborn as sns
import HB_module.outsourced as outs
try:
    import Ngl
    import HB_module.vertical_interpolation as vint
except ImportError:
    print('Library Ngl is not found on the system. Interpolation will not work. do not use -int option.')

sns.set_style('ticks')
#sns.set(rc={'axes.facecolor':'white'})

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

def plotter(vm,x,y,norm,cmap,logscale,show,figs):
    #fig=figure()
    print('plotter')
    fig = plt.figure(num=1,figsize=figs)
    if x.name != 'time' and y.name != 'time':
        xx,yy=np.meshgrid(x,y)
        if xx.shape!=vm.shape:
            vm=vm.transpose()
           
    clevels = outs.check_rangefile(rangefile,var,vm)
    print('color levels are: {0}'.format(clevels))
    
    if logscale:
        minimum = np.min(vm)
        norm=matplotlib.colors.LogNorm(vmin=minimum)
        clevels=None
        #clevels = np.logspace(minimum,maximum,num_cont)
#        minimum = np.log10(minimum)
#        maximum = np.log10(maximum)
#        vm = np.log10(vm)
    
    xl,yl = outs.make_labels(var,vm,x,y)
    
    gases = ['O3','HCL','CL','CLY','']
    """Unfortunately the time axis was not properly decoded, so I need to 
    handle plots involving time as axes in a special case"""
    if xax.name == 'lon' and yax.name == 'lat':
        map = Basemap(projection = 'cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='l')#projection='splaea',boundinglat=-45,lon_0=270,resolution='l')#(projection='ortho',lat_0=60.,lon_0=-60.)#projection = 'cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='l')
        map.drawcoastlines(linewidth=0.25)
        meridians = map.drawmeridians(np.arange(0,360,30))
        map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=14)
        parallels = map.drawparallels(np.arange(-80,81,20))
        map.drawparallels(parallels,labels=[1,0,0,0],fontsize=14)
    
        lons, lats = np.meshgrid(x,y)
        mx,my = map(lons,lats)
        CF = map.contourf(mx,my,vm,clevels,cmap=cmap,norm=norm)  
        xl = ''; yl=''          
    elif x.name != 'time' and y.name != 'time': 
        CF = plt.contourf(x,y,vm,levels=clevels,norm=norm,cmap=cmap)
        if args.noblack == False:        
            CS=plt.contour(x,y,vm,levels=clevels,colors='k',norm=norm)
        
        try:    
            timestamp = outs.make_timestamp(FileName)
        except AttributeError:
            try:
                timestamp=outs.make_timestamp_clim(FileName)
                timestamp=timestamp.strip('h0').strip('.')
            except AttributeError:
                timestamp = ''
        plt.title('Variable: {0}  Time: {1}'.format(var,timestamp),fontsize=18)
        
        plt.locator_params(axis='x',nbins=10)
    elif x.name == 'time':
        dummy_x=np.arange(0,len(x))
        CF = plt.contourf(dummy_x,y,vm.transpose(),levels=clevels,norm=norm,cmap=cmap)#norm=matplotlib.colors.LogNorm(vmin=minimum,vmax=maximum),cmap='jet')
        if args.noblack == False:         
            CS = plt.contour(dummy_x,y,vm.transpose(),levels=clevels,norm=norm,colors='k') #,norm=matplotlib.colors.LogNorm(),color='k')

        #plt.axis([0,len(x),len(y),0])
        #plt.yticks(range(0,len(y),13), ['{:E}'.format((y.values[i])) for i in range(0,len(y),13)], fontsize='18')
        if len(x) <= 10:    
            index, xtext = outs.parse_time_axis(x,len(x))
        else:
            index, xtext = outs.parse_time_axis(x,12)
            
        xtext = ['01-01', '02-01', '03-01', '04-01', '05-01', '06-01', '07-01', '08-01', '09-01', '10-01', '11-01','12-01']
        index=np.array([  0,  12,  24,  36,  48,  60,  72,  84,  96, 108, 120, 132])

        if 'control+' in FileName:
            xtext[0]='ctr-02-01' 
            plt.plot((dummy_x[11],dummy_x[11]),(y[0],y[len(y)-1]),color='k')
        
        plt.xticks(index.tolist(), xtext, fontsize='18')
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=45)
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
        
        if y.name == 'lev':
            yname = 'level'
        else:
            yname = y.name
#        clb.set_ticklabels(c)
        plt.title('{0}'.format(var),fontsize='18')
    elif y.name == 'time':
        print('functionality not yet implemented. Use the x-axis for time')
        sys.exit()        

    if y.name == 'lev':
        plt.yscale("log")
        plt.ylim(np.amax(y),np.amin(y))    
    
    plt.xlabel(xl, fontsize=18);plt.ylabel(yl,fontsize=18)

    cl = outs.clb_labels(var,ppm,ppb,ppt)
    if args.relative_anomalies:
        cl = '{0} percent change'.format(var)
    print(cl)
    
    clb = plt.colorbar(CF,format='%.3g');
    clb.set_label(cl,fontsize=18)
        #plt.figure(num=1,figsize=(20,10))   
    if show:            
        plt.show()
    title = '{0}_{1}_{2}{3}.png'.format(FileName,var,x.name,y.name)
    fig.savefig(title,bbox_inches='tight',figsize=figs,dpi=300)
    print('{0} was saved'.format(title))
    title = '{0}_{1}_{2}{3}.svg'.format(FileName,var,x.name,y.name)
    fig.savefig(title,bbox_inches='tight',figsize=figs,dpi=300)
    print('{0} was saved'.format(title))
    #title=('{0} at {1}={2} and {3}={4}'.format(var,getattr(v,pvar1)[p1],getattr(v,pvar1)[p1].values,getattr(v,pvar2)[p2],getattr(v,pvar2)[p2].values))
    #close(fig)    
    return

if __name__ == "__main__":
    desc='''
    This program takes the arguments described above and a NetCDF file and 
    plots a 2D filled contour plot of the data. The arguments describe what the 
    program will do to the data before plotting. All 4 spatio-temporal dimensions
    must be given (time, latitude, longitude, level) and the argument tells the 
    program how to treat that dimension. The possible values to the dimensional 
    arguments are: None if the axis is not present, xax (for assigning x-axis), yax (for y-axis), mean (for telling
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
    parser.add_argument('--xaxis_limits','-xlim',help='indices to limit a subsection of the x axis. The spcified axis will be indexed by these values',nargs=2, default=None,type=int)
    parser.add_argument('--yaxis_limits','-ylim',help='indices to limit a subsection of the y axis. The spcified axis will be indexed by these values',nargs=2, default=None,type=int)
    parser.add_argument('--Variable', '-v', help='Specify data variable field for plotting', default=None)
    parser.add_argument('--anomaly','-a', help='If set, the data are treated as anomalies from a mean state. Divergent color mapping will be applied', action='store_true')
    parser.add_argument('--index', '-i', help='Sets the program to index dimension by index. Slicing points should be given as integers', action='store_true')
    parser.add_argument('--logarithmic_colors', '-log', help='Sets logarithmic color scaling for the plotted field',action='store_true')
    parser.add_argument('--show','-s', help='display plot before saving', action='store_true')
    parser.add_argument('--rangefile',help='specify path to text file containing color ranges for the plot', default='ranges.dat')
    parser.add_argument('--figsize', help='Tuple specifying the figure size default=(10,4)',default='(10,4)')
    parser.add_argument('--activate_midpoint','-am', help='activate the possibility of setting midpoint normalization without diverging colormap',action='store_true')    
    parser.add_argument('--midpoint', help='Specify midpoint value for divergent colormap, default=0',default=0)
    parser.add_argument('--relative_anomalies', '-ra', help='If ser the data are treated as relative anomalies from mean state. Divergent color mapping and midpoint=1 will be applied',action='store_true')
    parser.add_argument('--noblack','-nb',help='if specified, removed black contourlines from the contourf plot', action='store_true')
    parser.add_argument('--vertical_interpolation','-int',help='toogle interpolation to pressure levels. Requires Ngl',action='store_true')
    
    args = parser.parse_args()
    
    show = args.show
    var = args.Variable
    assert var != None, 'Variable nedds to be specified by --Variable [-v] variable_name'
    
    rangefile = args.rangefile 
       
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
    
    #Check that all coordinates in the dataset are accounted for.
    for key,value in dims.items():
        try:
            v.coords[key]
            if dims[key] == None:
                print('{0} is present as a dimension in the dataset variable. Specify how to handle it at runtime'.format(key))
                sys.exit()
        except KeyError:
            if dims[key] != None:
                print('{0} is not present as a dimension in the dataset. Set it to None at runtime'.format(key))
                sys.exit()
        except AttributeError:
            if var == 'T':
                if key not in v.dims:
                    print('{0} is present as a dimension in the dataset variable. Specify how to handle it at runtime'.format(key))
                    sys.exit()
            else:
                print('SOMETHING IS WRONG!!!')
                sys.exit()
                
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
        
    if args.xaxis_limits != None:
        xlims = np.arange(args.xaxis_limits[0],args.xaxis_limits[1])
        x_lims = {}
        x_lims[xax.name]=xlims
        v = v[x_lims]
        xax = xax[xlims]
        
    if args.yaxis_limits != None:
        ylims = np.arange(args.yaxis_limits[0],args.yaxis_limits[1])
        y_lims = {}
        y_lims[yax.name]=ylims
        v = v[y_lims]
        yax = yax[ylims]
        
    if args.relative_anomalies:
        midpoint =0
    else:
        midpoint=float(args.midpoint)
            
    #Apply normalisation and color map for the plotting function
    velocities = ['U','V','OMEGA']
        
    if args.anomaly or var in velocities:
        cmap = sns.diverging_palette(220, 20,as_cmap=True)
        norm = MidpointNormalize(midpoint=midpoint)
    else:
        #cmap = sns.cubehelix_palette(start=.5, rot=-.75, light=1,dark=0.1, as_cmap=True)
        #cmap=sns.cubehelix_palette(light=1,as_cmap=True)
        #cmap = 'viridis'
        cmap = sns.cubehelix_palette(start=.5, rot=-.75,as_cmap=True)
        if args.activate_midpoint:
            norm = MidpointNormalize(midpoint=midpoint)
        else:
            norm = None
    
    figsize = args.figsize.strip('(').strip(')').split(',')
    figsize = [float(s) for s in figsize]
        
    if args.logarithmic_colors:
        logscale = True
    else:
        logscale = False
               
    print('pointvars ')
    print(pointvars)
    if args.vertical_interpolation: #interpolate to pressure levels. By default, the same levels as in the original data.
        print('Interpolating...')        
        plevo=np.array([1000,900,800,600,500,300,200,100,70,50,30,10,7,5,3,1])
        #plevo = v.lev
        v = vint.vertical_interpolation(v,plevo,data.hyam,data.hybm,data.PS,data.P0)
        yax = v.lev
        
    vm1 = v.mean(dim=meanvars)
    
    vm = vm1[pointvars]
    

    
    ppt = ['BRO','BROY','HBR']        
    ppb = ['CLOY','CLO','HCL']
    ppm = ['O3']
    um2pcm3 = ['sad_sage']

    if not args.relative_anomalies:
        if var in ppt:
            vm = vm*1e12
        elif var in ppb:
            vm = vm*1e9
        elif var in ppm:
            vm = vm*1e6
        elif var in um2pcm3:
            vm = vm*1e8
        elif var in ['T','TS']:
            if not args.anomaly:
                print("I'll subtract 273")
                vm = vm-273.15

    if args.relative_anomalies:
        vm = vm*100-100
    
    plotter(vm,xax,yax,norm,cmap,logscale,show,figsize)
    
    
