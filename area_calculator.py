# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 13:07:42 2015

@author: hanbre
"""
from __future__ import print_function
from math import *
import numpy as np

R=6378*1000 #Earth's radius
lat1=radians(12.31579) #latitude and longitude boundaries for the calculation
lat2=radians(16.10526)
lon1=268.5
lon2=272.5

P=29.728 #Midlayer pressure
P1=26.8825 #lower and upper pressure boundary
P2=32.5735
Rl=287 #Gas constant for dry air, representative for the stratosphere
T=235 #Temperature
g=9.81 #g
rho=P*100/(Rl*T) #Calculation of density

dz=(P2-P1)*100/(rho*g) #Elevation change between the pressure boundaries. Hydrostatic assumption

A=(pi/180)*R**2*(abs(sin(lat1)-sin(lat2))*abs(lon1-lon2)) #Area
print('A={0} m^2'.format(A))
V=dz*A #Volume
print('V={0} m^3'.format(V))
M=rho*V #Mass of air
print('M={0} kg'.format(M))

#HBr
dmol_frac = 32.65e-8
molar_mass = 80.91 # HBr=80.91, HCl=
mol_mass_air = 28.97
dmass_frac = dmol_frac*(molar_mass/mol_mass_air)
halog_frac = 0.987 #HBr=0.98, HCl = 
dmass = dmass_frac*M
dhalog_mass = dmass*halog_frac

print('Added Bromine mass from modification={0:E}'.format(dhalog_mass))

#HCl
dmol_frac = 22.7e-5
molar_mass = 36.46 # HBr=80.91, HCl=
mol_mass_air = 28.97
dmass_frac = dmol_frac*(molar_mass/mol_mass_air)
halog_frac = 0.972 #HBr=0.98, HCl = 
dmass = dmass_frac*M
dhalog_mass = dmass*halog_frac

print('Added Chlorine mass from modification={0:E}'.format(dhalog_mass))