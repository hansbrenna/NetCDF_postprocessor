# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:31:31 2015

@author: hanbre
"""

from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import xray
import datetime
import netCDF4
from mpl_toolkits.basemap import Basemap
import matplotlib
from matplotlib.pylab import *
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize
import seaborn as sns
from IPython import embed

class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

def read_data(id_in):
    data = xray.open_dataset(id_in)
    return data
    
    
    
def plotter(vm,x,y):
    #fig=figure()
    print('plotter')
    
    xx,yy=np.meshgrid(x,y)
    if shape(xx)!=shape(vm):
        vm=vm.transpose()
    
    gases = ['O3','HCL','CL','CLY','']
    if var in gases:
        CF = contourf(x,y,vm,linspace(np.amin(vm.values),np.amax(vm.values),10),cmap=matplotlib.cm.jet)
        CS=contour(x, y, vm,linspace(np.amin(vm.values),np.amax(vm.values),10),colors='k')
    elif var == 'T':
        CF = contourf(x,y,vm,linspace(np.amin(vm.values),400,10),cmap=matplotlib.cm.jet)
        CS=contour(x, y, vm,linspace(np.amin(vm.values),400,10),colors='k')
    else:
        norm = MidpointNormalize(midpoint=0)
        CF=contourf(x,y,vm,np.linspace(np.amin(vm.values),np.amax(vm.values),1000),norm=norm,cmap='seismic')
        CS=contour(x, y, vm,10,colors='k')
    xlabel(x.units);ylabel(y.units)
    clb = colorbar(CF); clb.set_label('('+v.units+')')
    #title=('{0} at {1}={2} and {3}={4}'.format(var,getattr(v,pvar1)[p1],getattr(v,pvar1)[p1].values,getattr(v,pvar2)[p2],getattr(v,pvar2)[p2].values))
    #close(fig)    
    return
    
def meaner(v,mvars):
    vm = v.mean(dim=mvars)
    return vm

def pointextr(v,pvar1,p1,pvar2,p2,pvars):
    vm = v[pvars]
    return vm
    
if __name__=='__main__':
    avgall=False; bandavg=False; point=False;
    if len(sys.argv)<5 or 'help' in sys.argv:
        print( 'This script takes at least 5 command line arguments ',len(sys.argv),' is given. \n')
        print( 'The usage is: Name of this script; path and name of netcdf file to be analysed;\n')
        print( 'name of variable; name of x-axis; name of y-axis (time, lev, lat, lon)')
        print( 'The 6th argumaent must be either point or band. If point')
        print( 'a point must be specified in the other two dimensions on the form (dim1 point1 dim2 point2)')
        sys.exit()
    elif len(sys.argv)==5:
          avgall = True
    elif len(sys.argv) > 5:
        if sys.argv[5] == 'band':
            bandavg = True
        if sys.argv[5] == 'cut':
            point = True
        if sys.argv[5] == 'point':
            point = True
            dim1 = sys.argv[6]
            point1 = double(sys.argv[7])
            dim2 = sys.argv[8]
            point2 = double(sys.argv[9])
        else:
            print( "If this script is given more than 5 command line arguments, sys.argv[5] has to be 'cut', 'point' or 'band'. Give 'help' as an argument to show help text.")
            sys.exit()
            
            id_in=sys.argv[1]
            ds=read_data(id_in)
            
            