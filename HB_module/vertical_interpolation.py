# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 09:57:42 2016

@author: hanbre
"""
from __future__ import print_function
import argparse
import sys
import numpy as np
import pandas as pd
import xarray as xr
import Ngl


def vertical_interpolation(da,lev_n, hya, hyb, PS, P0):
    """This function operates on xarray.DataArray objects. Uses Ngl vinth2p.
    Give the original data, the pressure levels to interpolate to, the hybrid 
    coefficients, surface and reference pressure. Returns a DataArray object"""
    nlev = len(lev_n)
    dummy = np.empty(shape=[len(da.time),nlev,len(da.lat),len(da.lon)])
    time = da.time; lat = da.lat; lon = da.lon;
    dan = xr.DataArray(dummy,coords=[time, lev_n, lat, lon],dims=da.dims)
    da.values = Ngl.vinth2p(da,hya,hyb,lev_n,PS,1,P0,1,False)
    return da    
    #Ngl.vinth2p call signature array = Ngl.vinth2p(datai, hbcofa, hbcofb, plevo, psfc, intyp, p0, ii, kxtrp)