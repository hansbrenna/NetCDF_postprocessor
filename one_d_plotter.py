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
    plt.title()

def get_data(ID):
    case_id = ID.split('/')
    dataset= rfm.read_data(ID)
    return dataset,case_id
        
if __name__ == '__main__':
    ds,case_id = get_data(sys.argv[1])
    
    xax = sys.argv[2]
    var = sys.argv[3]    
    
    x = getattr(ds,xax).values
    fx = getattr(ds,var).values
    
    if type(fx) != np.ndarray:
        fx = getattr(ds,var).values()      
        fx = fx[0]
        fx=fx.squeeze()
        fx=fx.values
    

    
    frame = pd.DataFrame(fx,index=x)
    
    if len(sys.argv)>4:
        skip = sys.argv[4]
    else:
        skip = 1
    
    frame.plot()
    if int(skip) == 0:
        s = raw_input('Title for plot: ')
        plt.title(s)
    plt.savefig('{0}/{1}_{2}_{3}.png'.format(case_id[0],case_id[1],xax,var),dpi=100)
    #plt.show()
    #one_d_plot(x,fx)
    
    
    
    
    