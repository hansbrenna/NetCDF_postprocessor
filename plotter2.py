# -*- coding: utf-8 -*-
"""
Created on Wed Jun 03 16:03:10 2015

@author: hanbre
"""

#Import required modules
from __future__ import print_function
import sys
import numpy as nmp
from mpl_toolkits.basemap import Basemap
import matplotlib
from matplotlib.pylab import *
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize
from netCDF4 import Dataset
import seaborn as sns

from IPython import embed

sns.set(style="dark")

def find_nearest(array,value):
    idx = (nmp.abs(array-value)).argmin()
    return array[idx]

class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))
        
def ExtractVariables(ID,var,xax,yax):
    x = id_in.variables[xax][:] ; # extracting x axis variable 1d
    xl = size(x)
    print( shape(x))
    
    y = id_in.variables[yax][:] ; # extracting y axis variable 1d
    yl = size(y)
    print( shape(y))
    
    xunits = id_in.variables[xax].units
    yunits = id_in.variables[yax].units

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
    
    print( ax)
    
    P = id_in.variables[var][:,:,:,:] ; # extracting 4D variable "var" (3D+T field) P=generic
    Punits = id_in.variables[var].units
#    embed()
    return x,y,P,Punits,ax,xunits,yunits
    
def plotfunc(var,mP,x,y,xunits,yunits,Punits):
    """
    docstring   
    """
    wo = 0.95 ; # width occupation for each figure (fraction)    
    
    xis = axes([0.09,  0.1,   0.85,       0.82], axisbg = 'white')
    
    xx,yy=nmp.meshgrid(x,y)
    print( 'Shape of meshgrid x and y axes is ',shape(xx), shape(yy))
    if shape(xx) != shape(mP):
        mP = transpose(mP)
        print( 'Shapes were unequal, so variable is transposed. New shape ', shape(mP))
        if shape(xx) != shape(mP):
            print( 'Shapes still unequal. Exiting...')
            sys.exit()
    
    if var == 'O3' or var == 'T':
        CF = contourf(x,y,mP,10,cmap=matplotlib.cm.copper)
        CS=contour(x, y, mP,10,colors='k')
    else:
        norm = MidpointNormalize(midpoint=0)
        CF = contourf(x,y,mP,linspace(nmp.amin(mP),nmp.amax(mP),1000),norm=norm,cmap='seismic')    
        CS=contour(x, y, mP,10,colors='k')
    
    axis([min(x), max(x), max(y), min(y)])
    xlabel(xunits); ylabel(yunits);
    clb = colorbar(CF); clb.set_label('('+Punits+')')
    #clabel(CS,inline=1,fontsize=8)
    return
      
def figplot(ID, var, xax, yax):

    fig = figure(num = 1, figsize=(10.,5.), dpi=None, facecolor='w', edgecolor='k')

    wo = 0.95 ; # width occupation for each figure (fraction)    
    
    xis = axes([0.09,  0.1,   0.85,       0.82], axisbg = 'white')
    
    P=None;x=None;y=None;Punits=None;ax=None;xunits=None;yunits=None;
    
    if yax == 'lev':
        xis.set_yscale("log")
    
    x,y,P,Punits,ax,xunits,yunits=ExtractVariables(ID,var,xax,yax)
    
#    embed()
    mP = nmp.mean(nmp.mean(P[:,:,:,:],axis=ax[1]),axis=ax[0])
    print( 'Shape of averaged variable array for plotting is',shape(mP))
    
    fig = figure(num = 1, figsize=(10.,5.), dpi=None, facecolor='w', edgecolor='k')
    plotfunc(var,mP,x,y,xunits,yunits,Punits)
    
    savefig(cf_in+var+xax+yax+'.png', dpi=100, facecolor='w', 
            edgecolor='w', orientation='portrait')
    print("{0}.png was {1:2.3f} saved".format(cf_in+var+xax+yax,1.52248621))

    close(fig)    
    
    return 0    
    
def bandplot(ID, var, xax, yax,dim,dmin,dmax):
    x,y,P,Punits,ax,xunits,yunits=ExtractVariables(ID,var,xax,yax)
    d1 = id_in.variables[dim][:]
    #embed()
    print( d1)
    
    nmin = find_nearest(d1,dmin)
    print( nmin)
    nmax = find_nearest(d2,dmax)
    print( nmax)
    
    

    return 0
    
def pointplot(ID, var, xax, yax,dim1,p1,dim2,p2):
    x,y,P,Punits,ax,xunits,yunits=ExtractVariables(ID,var,xax,yax)
    d1 = id_in.variables[dim1][:]
    #embed()
    print( d1)
    d2 = id_in.variables[dim2][:]
    print( d2)
    
    nearest1 = find_nearest(d1,p1)
    print( nearest1)
    nearest2 = find_nearest(d2,p2)
    print( nearest2)
    
    print( 'p1=' ,p1)
    #embed()
    index1 = nmp.where(d1==nearest1)
    print( index1)
    ind1 = index1[0][0]
    index2 = nmp.where(d2==nearest2)
    ind2 = index2[0][0]

    condition1 = zeros(shape = shape(d1))
    #embed()
    condition1[ind1]=1  
    condition2 = zeros(shape = shape(d2))
    condition2[ind2]=1 

    print( P.shape    )
    
    xP = nmp.compress(condition1,P,axis=ax[0])
    print( xP.shape)
    xP = nmp.compress(condition2,xP,axis=ax[1])
    print( xP.shape)
    xP = squeeze(xP)
    print( xP.shape)
    
    fig = figure(num = 1, figsize=(10.,5.), dpi=None, facecolor='w', edgecolor='k')

    wo = 0.95 ; # width occupation for each figure (fraction)    
    
    xis = axes([0.09,  0.1,   0.85,       0.82], axisbg = 'white')
    if yax == 'lev':
        xis.set_yscale("log")
    
    plotfunc(var,xP,x,y,xunits,yunits,Punits)
    
    savefig('{0}{1}{2}{3}_point_{4}={5:2.3f}{6}={7:2.3f}.png'.format(cf_in,var,xax,yax,dim1,nearest1,dim2,nearest2),
            dpi=100, facecolor='w', edgecolor='w', orientation='portrait')
    print( cf_in+var+xax+yax+'.png was saved' )

    close(fig)   
    return 0

if __name__ == "__main__":
    avgall=False; bandavg=False; point=False;
    if len(sys.argv) < 5 or 'help' in sys.argv:
        print( 'This script takes at least 5 command line arguments ',len(sys.argv),' is given. \n')
        print( 'The usage is: Name of this script; path and name of netcdf file to be analysed;\n')
        print( 'name of variable; name of x-axis; name of y-axis (time, lev, lat, lon)')
        print( 'The 6th argumaent must be either point or band. If point')
        print( 'a point must be specified in the other two dimensions on the form (dim1 point1 dim2 point2)')
        sys.exit()
    elif len(sys.argv) == 5:
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
            print( "If this script is given more than 5 command line arguments, sys.argv[5] has to be 'cut', 'point' or 'band'")
            sys.exit()
              
    cf_in = sys.argv[1]
    
    id_in = Dataset(cf_in)
    print( 'File ', cf_in, 'is open...\n')
    
    variable = sys.argv[2]
    if variable not in id_in.variables:
        print( 'no such variable in ', cf_in, '\n')
        print( id_in.variables)
        sys.exit()
    
    xax = sys.argv[3] #Usage: time, lev, lat, lon
    yax = sys.argv[4]
    
    if xax==yax:
        print( 'x-axis and y-axis are the same variable')
        sys.exit()
    
    if avgall:
        figplot(id_in,variable,xax,yax)

    if point:
        pointplot(id_in,variable,xax,yax,dim1,point1,dim2,point2)
    
    
