# -*- coding: utf-8 -*-
"""
Created on Wed Jun 03 16:03:10 2015

@author: hanbre
"""

#Import required modules
import sys
import numpy as nmp
from mpl_toolkits.basemap import Basemap
import matplotlib
from matplotlib.pylab import *
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize
from netCDF4 import Dataset

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
        
def figplot(ID, var, xax, yax):

    fig = figure(num = 1, figsize=(10.,5.), dpi=None, facecolor='w', edgecolor='k')

    wo = 0.95 ; # width occupation for each figure (fraction)    
    
    xis = axes([0.09,  0.1,   0.85,       0.82], axisbg = 'white')
    
    x = id_in.variables[xax][:] ; # extracting x axis variable 1d
    xl = size(x)
    print shape(x)
    
    y = id_in.variables[yax][:] ; # extracting y axis variable 1d
    yl = size(y)
    print shape(y)
    
    xunits = id_in.variables[xax].units
    yunits = id_in.variables[yax].units
    
    
    if yax == 'lev':
        xis.set_yscale("log")

       
    
    ax = [0,1,2,3]    
    
    if xax == 'time':
        ax.remove(0)
    if xax == 'lev':
        ax.remove(1)
    if xax == 'lat':
        ax.remove(2)
    if xax == 'lon':
        ax.remove(3)
        
    if yax == 'time':
        ax.remove(0)
    if yax == 'lev':
        ax.remove(1)
    if yax == 'lat':
        ax.remove(2)
    if yax == 'lon':
        ax.remove(3)
    
    print ax    
    
    P = id_in.variables[var][:,:,:,:] ; # extracting 4D variable "var" (3D+T field) P=generic
    Punits = id_in.variables[var].units
    #embed()
    mP = nmp.mean(nmp.mean(P[:,:,:,:],axis=ax[1]),axis=ax[0])
    print 'Shape of averaged variable array for plotting is',shape(mP)
    
    xx,yy=nmp.meshgrid(x,y)
    print 'Shape of meshgrid x and y axes is ',shape(xx), shape(yy)
    if shape(xx) != shape(mP):
        mP = transpose(mP)
        print 'Shapes were unequal, so variable is transposed. New shape ', shape(mP)
    
    norm = MidpointNormalize(midpoint=0)
    CF = contourf(x,y,mP,linspace(nmp.amin(mP),nmp.amax(mP),1000),norm=norm,cmap='seismic')    
    CS=contour(x, y, mP,10,colors='k')
    
    axis([min(x), max(x), max(y), min(y)])
    xlabel(xunits); ylabel(yunits);
    clb = colorbar(CF); clb.set_label('('+Punits+')')
    #clabel(CS,inline=1,fontsize=8)
    
    savefig(cf_in+var+xax+yax+'.png', dpi=100, facecolor='w', edgecolor='w', orientation='portrait')

    close(fig)    
    
    return 0    


if len(sys.argv) < 5:
    print 'This script takes 5 command line arguments only ',len(sys.argv),' is given. \n'
    print 'The usage is: Name of this script; path and name of netcdf file to be analysed;\n'
    print 'name of variable; name of x-axis; name of y-axis (time, lev, lat, lon)'
    sys.exit()

cf_in = sys.argv[1]

id_in = Dataset(cf_in)
print 'File ', cf_in, 'is open...\n'

variable = sys.argv[2]
if variable not in id_in.variables:
    print 'no such variable in ', cf_in, '\n'
    print id_in.variables
    sys.exit()

xax = sys.argv[3] #Usage: time, lev, lat, lon
yax = sys.argv[4]

if xax==yax:
    print 'x-axis and y-axis are the same variable'
    sys.exit()

figplot(id_in,variable,xax,yax)


    
    
