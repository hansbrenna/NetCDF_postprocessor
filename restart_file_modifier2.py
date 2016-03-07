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
    
def modify_data(ds,var,le,la,lo,value):
    consistent_sum = True
    if consistent_sum:
        getattr(ds,var)[dict(lat=la,lon=lo,lev=le)]=getattr(ds,var)[dict(lat=la,lon=lo,lev=le)]+value
    else:
        getattr(ds,var)[dict(lat=la,lon=lo,lev=le)]=value
    return ds

if __name__=='__main__':
    id_in = sys.argv[1]
    case_id = id_in.split('/')
    f1=open('{0}/modified/{1}_README'.format(case_id[0],case_id[1]),'w')
    ds = read_data(id_in)
    with open(sys.argv[2], 'r') as file_in:
        header=next(file_in)
        for line in file_in:
            l=line.strip('\n').split(' ')
            le = int(l[0]); la = int(l[1]); lo = int(l[2])
            var = str(l[3])
            value = float(l[4])
            print(getattr(ds,var)[dict(lat=la,lon=lo,lev=le)].values)
            before=getattr(ds,var)[dict(lat=la,lon=lo,lev=le)].values
            ds=modify_data(ds,var,le,la,lo,value)
            print(getattr(ds,var)[dict(lat=la,lon=lo,lev=le)].values)
            print('file {0}/modified/{1} has been modified by program restart_file_modifier2.py'.format(case_id[0],case_id[1]),file=f1)
            print('The changes take effect at lev={0}, lat={1}, lon={2} and the changed value is {3}={4} from {3}={5}'.format(le,la,lo,getattr(ds,var).name,getattr(ds,var)[dict(lat=la,lon=lo,lev=le)].values,before),file=f1)
    
    ds.to_netcdf(path='{0}/modified/{1}'.format(case_id[0],case_id[1]),mode='w',)
    f1.close()

