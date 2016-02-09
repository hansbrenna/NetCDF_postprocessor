# -*- coding: utf-8 -*-
"""
Created on Thu Feb 04 11:28:27 2016

@author: hanbre
"""

from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import xray
import netCDF4
import datetime as dt 
from netcdftime import datetime
import scipy
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from math import *
import restart_file_modifier2 as rfm


def one_d_plot(x, fx):
    plt.plot_date(x,fx)

def get_data(ID):
    case_id = ID.split('/')
    dataset= rfm.read_data(ID)
    return dataset,case_id
        
if __name__ == '__main__':
    ds,case_id = get_data(sys.argv[1])
    
    x = getattr(ds,sys.argv[2]).values
    fx = getattr(ds,sys.argv[3]).values
    
    
    frame = pd.DataFrame(fx,index=x)
    
    frame.plot()
    
    plt.savefig('{0}_{1}_{2}.png'.format(sys.argv[1],sys.argv[2],sys.argv[3]),dpi=100)
    #plt.show()
    #one_d_plot(x,fx)
    
    
    
    
    