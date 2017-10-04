# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 11:24:05 2017

@author: hanbre
Draft program to calculate radiative forcing from ozone changes
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
import re
import seaborn as sns
import HB_module.outsourced as outs

class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

def calculate_partial_ozone(ds):
    #ds
    #ds.O3
    O3_vmm = ds.O3
    O3_mmm = O3_vmm*(48.0/28.94)
    
    g=9.81
    P0 = 100000.0
    PS = ds.PS
    #hyai = ds.hyai
    #hybi = ds.hybi
    Plev = ds.lev_p*100
    levhi = xarray.open_dataset('/home/hanbre/norstore_project/O3_RF_CICERO/aerocom.OsloCTM2.A2.CTRL.monthly.levelheight.nc',decode_times=False)['levelheight']
    
    
    dp = np.empty(shape=O3_vmm.shape)
    
    dpa=xarray.DataArray(dp,coords=ds.O3.coords,dims=ds.O3.dims)
    
    for i in range(1,Plevi.shape[0]):
        dpa[dict(lev_p=i-1)]=Plevi[i-1]-Plevi[i]
        
    dpa[dict(lev_p=-1)]=0.0
    O3_t=O3_mmm*dpa/g
    
    pO3DU = O3_t/2.1415e-5
    
    ds2=pO3DU.to_dataset(name='pO3')
    ds3=ds.merge(ds2)
    ds3.pO3.attrs['units']='DU'
    ds3.pO3.attrs['long_name']='Partial ozone column in each layer in Dobson Units'
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

def concatenate_DataSet_N_times(ds,N):
    temp_ds = ds.copy(deep=True)
    for i in xrange(N):
        temp_ds = xarray.concat([temp_ds,ds],dim='time')
    return temp_ds

def calculate_anomalies(data,clim):
    return data-clim    
    
def calculate_RF(NRF,data):
    return NRF.values*data.values
    
if __name__ == "__main__":
    sns.set_style('ticks')
    parser = argparse.ArgumentParser()
    parser.add_argument('--climatology_file','-cf',help='path to climatology file to use as anomaly baseline')
    parser.add_argument('--total_RF','-trf',help='calculate and plot total RF over the scenario and also calculate parameterized RF from AOD',action='store_true')
    parser.add_argument('FileName')
    
    
    args = parser.parse_args()
    """Open data NetCDF file and calculate partial O3 in DU"""
    file_id = args.FileName
    data = xarray.open_dataset(file_id,decode_times=False)
    ds = calculate_partial_ozone(data)
    pO3 = ds['pO3']
    
    
    """Open climatology file, expand to correct size and calculate partial O3"""    
    clim_data = xarray.open_dataset(args.climatology_file,decode_times=False)
    clim = calculate_partial_ozone(clim_data)
    clim_O3 = clim['pO3']
    clim_concat = get_clim_with_same_dims(pO3,clim_O3)
    clim_concat['time']=ds.pO3.time
    print(clim_data['O3'][dict(time=1,lat=1,lon=1)])
    
    """Calculate anomalies"""
    pO3_anom = calculate_anomalies(pO3,clim_concat)
    
    
    """Get NRF on same dimensions"""
    NRF_data = xarray.open_dataset('/home/hanbre/norstore_project/O3_RF_CICERO/NRFO3v6_OsloRF.nc',decode_times=False)
    NRF_concat = concatenate_DataSet_N_times(NRF_data,11)
    NRF_concat['time']=ds.pO3.time
    
    """Calculate sw_cloud RF"""
    sw_cloud_NRF = NRF_concat['SW_cloudy']
    sw_cloud_RF = calculate_RF(sw_cloud_NRF,pO3_anom)
#    print('SW \n')
#    print(sw_cloud_RF[1,:,1,1])
    
    """Calculate lw_adj_cloudy RF"""
    lw_adj_cloud_NRF = NRF_concat['LW_adj_cloudy']
    lw_adj_cloud_RF = calculate_RF(lw_adj_cloud_NRF,pO3_anom)
#    print('LW \n')
#    print(lw_adj_cloud_RF[1,:,1,1])
    
    """Put component RFs into DataArray structures"""
    lw_RF = xarray.DataArray(lw_adj_cloud_RF,coords=pO3.coords,dims=pO3.dims) 
    sw_RF = xarray.DataArray(sw_cloud_RF,coords=pO3.coords,dims=pO3.dims) 
    
    """Sum components over levels"""
    cum_lw_RF = lw_RF.sum(dim='lev_p')
    cum_sw_RF = sw_RF.sum(dim='lev_p')
    
    """zonal mean components"""
    zcum_lw_RF = cum_lw_RF.mean(dim='lon')
    zcum_sw_RF = cum_sw_RF.mean(dim='lon')
    
    """global mean cumulative component radiative forcings"""
    glob_lw_RF = zcum_lw_RF.reduce(np.average,dim='lat',weights=data['gw'].values)
    glob_sw_RF = zcum_sw_RF.reduce(np.average,dim='lat',weights=data['gw'].values)

    """Calculate net O3 RF"""
    net_RF = sw_cloud_RF+lw_adj_cloud_RF

    """Put the net_RF back into a xarray DataArray object"""
    RF = xarray.DataArray(net_RF,coords=pO3.coords,dims=pO3.dims) 
    #print(RF[dict(time=1,lat=1,lon=1)])
    
    """Cumulative RF over levels"""
    cumRF = RF.sum(dim='lev_p')
    
    """zonal mean cumulative RF"""
    zcumRF = cumRF.mean(dim='lon')


    
    """Global mean cumulative RF"""
    globRF = zcumRF.reduce(np.average,dim='lat',weights=data['gw'].values)
    
    globRF.plot()
    
    plt.figure()
    cmap = sns.diverging_palette(220, 20,as_cmap=True)
    norm = MidpointNormalize(midpoint=0)
    zcumRF.plot.contourf(levels=15)
    #plt.contourf(zcumRF.lat,zcumRF.time,zcumRF,cmap=cmap,norm=norm)
    #clb=plt.colorbar()    
    
#    plt.show()
    pandas_globRF = globRF.to_pandas()
    
    
    if args.total_RF:
        trf=plt.figure()
        aod_data = xarray.open_dataset('/home/hanbre/norstore_project/BCKUP_after_21.07.15/aCAVA_experiment/full_forcing/ensemble_average_h0_files/anomalies/f1850w.aCAVA_full.ens.anom.cam.h0.0001-0012.AOD.hormean.nc',decode_times=False)
        tot_RF_data = xarray.open_dataset('/home/hanbre/norstore_project/BCKUP_after_21.07.15/aCAVA_experiment/full_forcing/ensemble_average_h0_files/anomalies/f1850w.aCAVA_full.ens.anom.cam.h0.0001-0012.netradfluxt.hormean.nc',decode_times=False)
        tot_RF = tot_RF_data['FSNT']-tot_RF_data['FLNT']
        aod_RF = (-24*aod_data['AEROD_v'])
        aod_RF.name=None
        tot_RF.plot(label='Radiation imbalance')
        aod_RF.plot(label='AOD RF: RF=-24*AOD')
        (globRF/1000).plot(label='RF from O3 change')
        calcRF=(aod_RF+globRF/1000)
        calcRF.plot(label='AOD+O3 RF')
        plt.legend()
        
        
    
    plt.show()
    trf.savefig('radiative_forcing_comparisons.png',dpi=300)
    
        