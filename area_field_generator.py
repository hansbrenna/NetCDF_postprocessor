# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 13:50:24 2016

@author: hanbre
"""

from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import xray
import netCDF4
import restart_file_modifier2 as rfm
import scipy
import matplotlib
import matplotlib.pyplot as plt
from math import *


def eq2act_area(lat,lon):
    radlon1 = np.zeros(lon,dtype='f')
    radlon2 = np.zeros(lon,dtype='f')
    sinlat1 = np.zeros(lat,dtype='f')
    sinlat2 = np.zeros(lat,dtype='f')
    surface_area = np.zeros([lat,lon],dtype='f')
    factor_surface = np.zeros([lat,lon],dtype='f')
    earth_radius=6367.4447              # This value is from Wolfram Alpha
    radian_conversion = np.pi/180.0

    #At the specified resolution how many degrees per a pixel?
    pixlon=360./float(lon)
    pixlat=180./float(lat)
    print('Grid resolution is',pixlat,'x',pixlon,' (Units = Degree)')
    
    for j in xrange(lon):
        radlon1[j] = (((j+1) * pixlon) - pixlon)  * radian_conversion
        radlon2[j] = ((j+1) * pixlon) * radian_conversion

   # print(radlon1,'  ',radlon2)

    for i in xrange(lat):
        sinlat1[i]= sin(((((i+1)*pixlat)-pixlat)-90.0) * radian_conversion)
        sinlat2[i]= sin((((i+1)*pixlat)-90.) * radian_conversion)
    
    for i in xrange(lat):
        for j in xrange(lon):
            surface_area[i,j]=(earth_radius*earth_radius)*(radlon2[j]-radlon1[j])*(sinlat2[i]-sinlat1[i]) 
            print(radlon2[j]-radlon1[j])

    # Check everything is okay by calculating the Earth's surface area.
    total_area=0.0   
    for i in xrange(lat):
        for j in xrange(lon):
            total_area=total_area+surface_area[i,j]

    print( 'Calculated area of Earth =',total_area,'km')
    print( 'Actual value should be 5.1x10^8 km^2 ')
    
    # Crucially, create an array to use to weight gridded data      
    for i in xrange(lat):
        for j in xrange(lon):
            factor_surface[i,j]=surface_area[i,j]/surface_area[lat/2,lon/2]
    print( 'Center of grid = ',surface_area[lat/2,lon/2],'km^2 : weight = ',factor_surface[lat/2,lon/2])
    print( 'Edge of grid = ',surface_area[0,lon/2],'km^2 : weight = ',factor_surface[0,lon/2])
    return surface_area,factor_surface

def calculate_area(lat,lon):
    R=6367.4447 
    print('Grid resolution is',lat[2]-lat[1],'x',lon[2]-lon[1],' (Units = Degree)') 
    radlons = np.radians(lon.data)
    radlons2 = np.radians(lon.data - 2.5)
    sinlats = np.sin(lat.data)
    llat = len(lat); llon = len(lon)
    
    surface_area = np.zeros([llat,llon])    
    surfc = np.zeros([llat])

    surfc[:] = R*R*(radlons[1])*(sinlats[1:llat]-sinlats[0:llat-1])
    
    for i in xrange(llon):
        surface_area[:,i] =  surfc
        
    total=sum(sum(surface_area))
    print('total: ',total)
    return surface_area

id_in = sys.argv[1]
ds=rfm.read_data(id_in)

lats = ds.lat
lons = ds.lon

#area,weight = eq2act_area(lats,len(lons))
weight = calculate_area(lats,lons)

plt.contourf(lons,lats,weight,1000)
plt.title(r'The surface factor for each grid cell ')
plt.colorbar()