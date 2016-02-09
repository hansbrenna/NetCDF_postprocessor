# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:05:03 2015

@author: hanbre
"""

from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import xray
import netCDF4


def read_data(id_in):
    data = xray.open_dataset(id_in)
    return data
    
def modify_data(ds,le,la,lo,value):
    ds.HCL[dict(lat=la,lon=lo,lev=le)]=ds.HCL[dict(lat=la,lon=lo,lev=le)]*100
    ds.HBR[dict(lat=la,lon=lo,lev=le)]=ds.HBR[dict(lat=la,lon=lo,lev=le)]*100
    return ds
    

id_in = sys.argv[1]
case_id = id_in.split('/')
le = int(sys.argv[2]); la = int(sys.argv[3]); lo = int(sys.argv[4])
value = float(sys.argv[5])
ds = read_data(id_in)
print(ds.HCL[dict(lat=la,lon=lo,lev=le)].values)
ds=modify_data(ds,le,la,lo,value)
print(ds.HCL[dict(lat=la,lon=lo,lev=le)].values)

if 'modified' in case_id[0] or 'modified' in case_id[1]:
    ds.to_netcdf(path='{0}/modified/{1}'.format(case_id[0],case_id[2]),mode='w',)
    f1=open('{0}/modified/{1}_README'.format(case_id[0],case_id[2]),'a')
    print( 'a')
else:
    ds.to_netcdf(path='{0}/modified/{1}'.format(case_id[0],case_id[1]),mode='w',)
    f1=open('{0}/modified/{1}_README'.format(case_id[0],case_id[1]),'a')
    print( 'b')

print('file {0}/modified/{1} has been modified by program restart_file_modifier.py'.format(case_id[0],case_id[1]),file=f1)
print('The changes take effect at lev={0}, lat={1}, lon={2} and the changed values are HCL={3} and HBR={4}'.format(le,la,lo,ds.HCL[dict(lat=la,lon=lo,lev=le)].values,ds.HBR[dict(lat=la,lon=lo,lev=le)].values),file=f1)
f1.close()
