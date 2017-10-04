# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 16:26:41 2016

@author: hanbre
"""

from __future__ import print_function
import sys
import argparse
import netcdftime
import numpy as np
import pandas as pd
import xarray
import netCDF4
import matplotlib
from mpl_toolkits.basemap import Basemap, shiftgrid, addcyclic
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import Normalize
from matplotlib import gridspec
import re
import seaborn as sns
import HB_module.outsourced as outs

sns.set_style('ticks')
matplotlib.rcParams['xtick.labelsize']=14
matplotlib.rcParams['ytick.labelsize']=14

class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

def calculate_total_ozone(ds):
    #ds
    #ds.O3
    O3_vmm = ds.O3
    O3_mmm = O3_vmm*(48.0/28.94)
    
    g=9.81
    P0 = ds.P0
    PS = ds.PS
    hyai = ds.hyai
    hybi = ds.hybi
    Plevi = hyai*P0+hybi*PS
    
    dp = np.empty(shape=O3_vmm.shape)
    
    dpa=xarray.DataArray(dp,coords=ds.O3.coords,dims=ds.O3.dims)
    
    for i in range(1,Plevi.shape[0]):
        dpa[dict(lev=i-1)]=Plevi[i]-Plevi[i-1]
        
    O3_t=O3_mmm*dpa/g
    
    totO3=O3_t.sum(dim='lev')
    
    totO3DU = totO3/2.1415e-5
    print('Minimum column ozone value: {}'.format(totO3DU.min()))
    ds2=totO3DU.to_dataset(name='totO3')
    ds3=ds.merge(ds2)
    ds3.totO3.attrs['units']='DU'
    ds3.totO3.attrs['long_name']='Column ozone in Dobson Units'
    return ds3
    
def get_clim_with_same_dims(data, clim):
    target = data.shape
    current = clim.shape
    temp_clim = clim.copy(deep=True)
    counter = 0
    while current != target:
        temp_clim = xarray.concat([temp_clim,clim],dim='time')
        current = temp_clim.shape
        counter += 1
        if counter >= 100:
            print('Could not make climatological data match shape of exp data. Tried {} times'.format(counter))
            sys.exit()
#        print(current)
#        print(target)
    return temp_clim

def calculate_anomalies(data,clim):
    return data-clim

def calculate_relative_anomalies(data,clim):
    return data/clim

def calculate_increase_in_uv(data):
    raf = 2.2#1.2 #after Madronich et al.
    dUV = data**(-raf)
    return (dUV-1)*100
   
def latitude_bands_time_series(data,gw,clabel):
    dlat = [10.0,30.0,60.0,90.0,180.0]
    lat0 = -90.0
    latm = 90.0
    for dl in dlat:
        with sns.color_palette('husl',int(180.0/dl)):
            plt.figure()
            lat1 = lat0
            lat2 = 0.0
            while lat1 < latm:
                lat2 = lat1+dl    
                data.sel(lat=slice(lat1,lat2)).reduce(np.average,dim='lat',weights=gw.sel(lat=slice(lat1,lat2))).plot(label='{},{}'.format(lat1,lat2))
                lat1 = lat2
            plt.legend()
            plt.ylabel(clabel)

if __name__ == "__main__":
    sns.set_style('ticks')
    parser = argparse.ArgumentParser()
    group_projections = parser.add_mutually_exclusive_group()
    group_projections.add_argument('--time_lat','-tl',help='set mode to time vs. latitude',action='store_true')
    group_projections.add_argument('--projection','-p',help='set map projection. Valid: sp (Antarctic, default), np (Arctic)',default='sp')
    group_anoms = parser.add_mutually_exclusive_group()
    group_anoms.add_argument('--calculate_anomaly','-ca', help='set mode to calculate absolute anomalies',action='store_true')
    group_anoms.add_argument('--calculate_relative_anomaly','-ra', help='set mode to calculate relative anomalies',action='store_true')
    parser.add_argument('--climatology_file','-cf',help='path to climatology file to use as anomaly baseline')
    parser.add_argument('--uv_change','-uv',help='tell the program to calculate the change in ultraviolet radiation. Requires -ra option',action='store_true')
    parser.add_argument('--colorbar','-cb',help='toggle colorbar on',action='store_true')    
    parser.add_argument('--title',help='Set the plot title text',default=False)
    parser.add_argument('--show','-s',help='show the figure',action='store_true')
    parser.add_argument('--decode_time','-dec_t',help='decode time variable according to CF conventions',action='store_true')
    parser.add_argument('--cloud_cover','-cc',help='Specify a path to NetCDF file containing a cloud cover field.tells the program to calculate the uv change modified by clouds. Requires uv',default=False)
    parser.add_argument('--lat_bands_time_series','-ts',help='Tell the program to calculate latitude band time series and plot them in a separate figure. Requires -tl',action='store_true')
    group_abs_on_anoms = parser.add_mutually_exclusive_group()
    group_abs_on_anoms.add_argument('--abs_on_anomalies','-aon',help='Plot absolute field values in black on colormap of anomalies. Requires -ca or -ra options', action='store_true')
    group_abs_on_anoms.add_argument('--hole_on_anomalies','-220',help='Plot the 220 DU contour line on anomaly plot',action='store_true')
    parser.add_argument('FileName')
    

    args = parser.parse_args()
    
    file_id = args.FileName
    if args.time_lat:
        tl = True
    else:
        tl = False
    if args.decode_time:
        print('attempting to decode times as datetimes')
        data = xarray.open_dataset(file_id)
        print(data.time[0:5])
    else:
        data = xarray.open_dataset(file_id,decode_times=False)
    ds3 = calculate_total_ozone(data)
    
    gw = data['gw']
    
    if args.abs_on_anomalies or args.hole_on_anomalies:
        assert args.calculate_anomaly or args.calculate_relative_anomaly, 'if -aon or -220 is given either -ca or -ra needs to be set as well'
        ds3_bckup = ds3.copy(deep=True)
        var_aoa = ds3_bckup.totO3
        if args.abs_on_anomalies:
            aon = True
            hoa = False
        if args.hole_on_anomalies:
            hoa = True
            aon = False
    else:
        aon = False
        hoa = False
    
    if args.cloud_cover:
        assert args.uv_change, 'Must give uv_change flag to use cloud cover'
        cc_data = xarray.open_dataset(args.cloud_cover,decode_times=False)
        cc = cc_data['CLDTOT']
        
    if args.lat_bands_time_series:
        assert tl == True, 'Plotting time series for latitude bands requires -tl option'
    
    clabel='Column O3 [DU]'
    colorbar = args.colorbar
    if colorbar:
        cb_info = '_cb'
    else:
        cb_info = ''
    
    valid_projections = ['sp','np']
    projection = args.projection
    assert projection in valid_projections, 'Invalid projection given. Valid projection options are {}'.format(valid_projections)
    
    if args.uv_change:
        assert args.calculate_relative_anomaly == True, 'to calculate uv change relative O3 anomalies are needed. set -ra at runtime'
    if args.calculate_anomaly or args.calculate_relative_anomaly:
        assert args.climatology_file != None, 'when calculating anomalies a climatology file must be specified'
        clim_data = xarray.open_dataset(args.climatology_file,decode_times=False)
        clim = calculate_total_ozone(clim_data)
        clim_O3 = clim['totO3']
        clim_concat = get_clim_with_same_dims(ds3['totO3'],clim_O3)
        clim_concat['time']=ds3.totO3.time
        
        cmap = sns.diverging_palette(220, 20,as_cmap=True)
        
        if args.calculate_anomaly:
            tot_O3_anom = calculate_anomalies(ds3['totO3'],clim_concat)
            var = tot_O3_anom
            norm = MidpointNormalize(midpoint=0)
            clabel='Change in column O3 (DU)'
            clevels=np.array([-200,-160,-120,-80,-40,0,40])
        elif args.calculate_relative_anomaly:
            tot_O3_anom = calculate_relative_anomalies(ds3['totO3'],clim_concat)
            var = (tot_O3_anom-1)*100
            norm = MidpointNormalize(midpoint=0)
            clabel='Change in column O3 (%)'
            clevels = None
            if args.uv_change:
                uv_change = calculate_increase_in_uv(tot_O3_anom)
                var = uv_change
                if args.cloud_cover:
                    var = uv_change*cc
                norm = MidpointNormalize(midpoint=0)
                clevels = np.array([-40,-20,0,20,40,100,160,220,280,340,400])#np.linspace(-40,240,8)# np.array([80,90,95,105,120,130,160,200,240,280,320])
                clabel='Change in biologically active UV (%)'
    else:
        var = ds3.totO3
        clevels=np.linspace(100,460,19)
        #cmap=sns.cubehelix_palette(light=1, as_cmap=True)
        cmap = sns.cubehelix_palette(start=.5, rot=-.75,as_cmap=True)
        norm=None
        
    x = ds3.lon; y = ds3.lat

    #cmap='viridis'
    
    ######Output image file name parameters:##########
    if args.uv_change:
        extra_info = '_uv'
        if args.cloud_cover:
            extra_info = '_uv_cc'
    elif args.calculate_relative_anomaly:
        extra_info = '_ra'
    elif args.calculate_anomaly:
        extra_info = '_ca'
    else:
        extra_info = ''
    
    if aon:
        more_info = '_aoa'
    elif hoa:
        more_info = '_hoa'
    else:
        more_info = ''
    
    
    if tl == True:
        #sns.set(font_scale=1.5)
#        clevels = np.linspace(100,460,19)
        fig_tl = plt.figure(figsize=(10,5))
        gs = gridspec.GridSpec(2, 1, height_ratios=[50, 1]) 
        var = var.mean(dim='lon')
        if args.decode_time == False:
            var['time']=np.arange(var.time.shape[0])
    #    var.plot.contourf(x='time',y='lat',cmap=cmap)
        if args.decode_time:
            CF=var.plot.contourf(x='time',y='lat',levels=clevels,cmap=cmap,add_colorbar=False)
        else:
            CF = plt.contourf(var.time,var.lat,var.transpose(),levels=clevels,cmap=cmap,norm=norm,extend="max")
            if args.calculate_anomaly == False and args.calculate_relative_anomaly == False:
                CS = plt.contour(var.time,var.lat,var.transpose(),np.linspace(220,220,1),colors='k')
                #plt.clabel(CS,(220),fmt='%1.0f',inline=True)
        if aon: #if absolute on anomalies
            var_aoa = var_aoa.mean(dim='lon')
            var_aoa['time']=np.arange(var_aoa.time.shape[0])
            CS = plt.contour(var.time,var.lat,var_aoa.transpose(),np.linspace(100,460,10),colors='k')
            for c in CS.collections:
                c.set_linestyle('solid')
                c.set_linewidth(1)
        elif hoa: #if 220 isoline on anomalies
            CS = plt.contour(var.time,var.lat,var_aoa.transpose(),np.linspace(220,220,1),colors='k')
            plt.clabel(CS,(220),fmt='%1.0f',inline=True)
        else:
            if args.decode_time:
                CS=var.plot.contour(x='time',y='lat',levels=np.linspace(220,220,1),colors='k',add_colorbar=False)
            else:
                if hoa:
                    CS = plt.contour(var.time,var.lat,var.transpose(),np.linspace(220,220,1),colors='k')
        if aon:
            plt.clabel(CS,(140,220,300,380,460),fmt='%1.0f',inline=False)
        if colorbar:        
            clb=plt.colorbar(CF) 
            clb.set_label(clabel)#'Column O3 [DU]')
        if args.decode_time == False:
            text = ['J','A','J','O']
            locs = np.arange(0,145,3)
            labels = 12*text
            plt.xticks(locs,labels)
        #plt.xlim(0,143)
        plt.xlabel('Month',fontsize=16)
        plt.ylabel('Latitude',fontsize=16)
        if args.title != False:
            plt.title(args.title,fontsize=18)
        if args.lat_bands_time_series:
            latitude_bands_time_series(var,gw,clabel)
        plt.show()
        fig_tl.savefig('{0}{1}{2}{3}_ozone_timelat.png'.format(file_id,extra_info,more_info,cb_info),dpi=300,bbox_inches='tight')
        fig_tl.savefig('{0}{1}{2}{3}_ozone_timelat.svg'.format(file_id,extra_info,more_info,cb_info),dpi=300,bbox_inches='tight')
    else:
        var = var.isel(time=0)
        var,x_cyc = addcyclic(var,x)
        if aon or hoa:
            var_aoa = var_aoa.isel(time=0)
            var_aoa,x_cyc_aoa = addcyclic(var_aoa,x)
        fig_map=plt.figure()
        map = Basemap(projection = 'cyl',llcrnrlat=-40,urcrnrlat=40,llcrnrlon=0,urcrnrlon=360,resolution='l')#projection='splaea',boundinglat=-45,lon_0=270,resolution='l')#(projection='ortho',lat_0=60.,lon_0=-60.)#projection = 'cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='l')
        map.drawcoastlines(linewidth=0.25)
        meridians = map.drawmeridians(np.arange(0,360,30))
        map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=14)
        parallels = map.drawparallels(np.arange(-80,81,20))
        map.drawparallels(parallels,labels=[1,0,0,0],fontsize=14)
        
        lons, lats = np.meshgrid(x_cyc,y)
        mx,my = map(lons,lats)
        CF = map.contourf(mx,my,var,levels=clevels,cmap=cmap,norm=norm,vmin=np.min(clevels),vmax=np.max(clevels))
        if aon: #if absolute on anomalies
            CS = map.contour(mx,my,var_aoa,levels=np.linspace(100,460,10),colors='k')
            plt.clabel(CS,(140,220,300,380,460),fmt='%1.0f',inline=False)
            for c in CS.collections:
                c.set_linestyle('solid')
                c.set_linewidth(1)
        elif hoa:
            CS = map.contour(mx,my,var_aoa,np.linspace(220,220,1),colors='k')
            plt.clabel(CS,fmt='%1.0f',inline=True)
        else:
            CS = map.contour(mx,my,var,np.linspace(220,220,1),colors='k')
        if colorbar:        
            clb=plt.colorbar(CF,orientation='horizontal',fraction=0.05,shrink=0.65,pad=0.07)
            clb.set_label(clabel,fontsize=18)
            
        if args.title == False:
            try:
                timestamp=outs.make_timestamp(file_id)
                plt.title('Column O3 Time: {0}'.format(timestamp),fontsize=18)
            except:
                timestamp = 'dummy'
                plt.title('Column O3 Control',fontsize=18)
        else:
            plt.title(args.title,fontsize=18)
            
        fig_map.savefig('{0}{1}{2}{3}_ozone_map.png'.format(file_id,extra_info,more_info,cb_info),bbox_inches='tight',figsize=(14,4),dpi=300)
        
        fig=plt.figure()
        #lons, lats = np.meshgrid(x,y)
        #var, lons = shiftgrid(lon0 = 300., datain =var , lonsin = lons, start = True, cyclic = 360.)
        if projection == 'sp':
            map = Basemap(projection='spaeqd',boundinglat=-40,lon_0=180,resolution='l')#Basemap(projection='ortho',lat_0=-60,lon_0=180,resolution='l')#(projection='hammer',lon_0=180,resolution='c')#Basemap(projection='spaeqd',boundinglat=-10,lon_0=270,resolution='l')#(projection='splaea',boundinglat=-45,lon_0=270,resolution='l')#(projection='ortho',lat_0=60.,lon_0=-60.)#projection = 'cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='l')
        elif projection == 'np':
            map = Basemap(projection='npaeqd',boundinglat=40,lon_0=0,resolution='l')
        map.drawcoastlines(linewidth=0.25)
        meridians = map.drawmeridians(np.arange(0,360,30))
        map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=14)
        parallels = map.drawparallels(np.arange(-80,81,20))
        map.drawparallels(parallels,labels=[1,0,0,0],fontsize=14)
        
        mx,my = map(lons,lats)
        CF = map.contourf(mx,my,var,levels=clevels,cmap=cmap,norm=norm,vmin=np.min(clevels),vmax=np.max(clevels))
        if aon: #if absolute on anomalies
            CS = map.contour(mx,my,var_aoa,levels=np.linspace(100,460,10),colors='k')
            plt.clabel(CS,(140,220,300,380,460),fmt='%1.0f',inline=False)
            for c in CS.collections:
                c.set_linestyle('solid')
                c.set_linewidth(1)
        elif hoa:
            CS = map.contour(mx,my,var_aoa,np.linspace(220,220,1),colors='k')
            plt.clabel(CS,fmt='%1.0f',inline=True)
        else:
            CS = map.contour(mx,my,var,np.linspace(220,220,1),colors='k')
        if colorbar:        
            clb=plt.colorbar(CF,orientation='horizontal',fraction=0.05,shrink=0.65,pad=0.07)
            clb.set_label(clabel,fontsize=18)
        if args.title == False:
            try:
                timestamp=outs.make_timestamp(file_id)
                plt.title('Column O3 Time: {0}'.format(timestamp),fontsize=18)
            except:
                timestamp = 'dummy'
                plt.title('Column O3 Control',fontsize=18)
        else:
            plt.title(args.title,fontsize=18)
        if args.show:            
            plt.show()
        fig.savefig('{0}_{1}{2}{3}{4}_ozone_hole.png'.format(file_id,projection,extra_info,more_info,cb_info),bbox_inches='tight',dpi=300)
        fig.savefig('{0}_{1}{2}{3}{4}_ozone_hole.eps'.format(file_id,projection,extra_info,more_info,cb_info),bbox_inches='tight',dpi=300)
