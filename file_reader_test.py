# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:31:51 2015

@author: hanbre
"""
with open('files/test.dat') as f:
    for line in f:
        d=line.strip('\n').split(' ')
        print d