# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:32:58 2015

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
    i=0
    #case_id = id_in.split('/')
    with open(sys.argv[1], 'r') as file_in:
        header=next(file_in)
        for line in file_in:
            i+=1
            l=line.strip('\n').split(' ')
            id_in=l[0]
            ds=read_data(id_in)
            typ = l[1] 
            print(typ)
            var = l[2]
            xvar = l[3]; yvar = l[4]
            v=getattr(ds,var)
            x=getattr(ds,xvar)
            y=getattr(ds,yvar)
            if typ == 'm':
                print('here')
                mvar1 = l[5]; mvar2 = l[6]
                if size(v.dims)==4:
                    mvars = [mvar1,mvar2]
                else:
                    mvars = [mvar1]
                vm=meaner(v,mvars)
                savestring = '{0}{1}{2}{3}{4}{5}{6}.png'.format(id_in,typ,var,xvar,yvar,mvar1,mvar2)
                print(savestring)
            elif typ == 'p':
                print('there')
                pvar1=l[5]; p1=int(l[7])
                pvar2=l[6]; p2=int(l[8])
                pvars = {pvar1: p1, pvar2: p2}
                vm=pointextr(v,pvar1,p1,pvar2,p2,pvars)
                savestring = '{0}{1}{2}{3}{4}{5}{6}{7}{8}.png'.format(id_in,typ,var,xvar,yvar,pvar1,pvar2,p1,p2)
                print(savestring)
            xis = axes([0.09,  0.1,   0.85,       0.82], axisbg = 'white')
            fig = figure(num = i, figsize=(10.,5.), dpi=None, facecolor='w', edgecolor='k')
            plotter(vm,x,y)
            
            if yvar == 'lev':
                print('log=True')
                xis.set_yscale("log")
            savefig(savestring,dpi=100, facecolor='w', edgecolor='w', orientation='portrait')
            print('again')
            close(fig)
            del(ds)
        
    