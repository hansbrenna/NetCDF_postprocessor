from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt

def surface_area(lat, lon, chatty=True):
    def area_of_cell(radlon1, radlon2, sinlat1, sinlat2, R=6367.4447):
        """Calculate the surface area of a gridcell. R = earth radius"""
        return (R**2)*(radlon2-radlon1)*(sinlat2-sinlat1) 
    surface_area = np.zeros([lat, lon])
    factor_surface = np.zeros([lat, lon])
    pixlon=360./lon  #How many degrees per pixel?
    pixlat=180./lat
    rl1 = [(((x+1) * pixlon) - pixlon) * np.pi / 180.0 for x in range(lon)]
    rl2 = [((x+1) * pixlon) * np.pi / 180.0 for x in range(lon)]    
    sl1 = [np.sin(((((x+1)*pixlat)-pixlat) -90.0) * np.pi / 180.0) for x in range(lat)]
    sl2 = [np.sin((((x+1)*pixlat) -90.) * np.pi / 180.0) for x in range(lat)]
    for i in range(lat):
        surface_area[i,0]=area_of_cell(rl1[0], rl2[0], sl1[i], sl2[i]) 
        surface_area[i,1:] = surface_area[i,0]  # repeat the first column along the array
    total_area = np.sum(surface_area)
    assert abs(total_area - 510100000) < 1000000, "Error: Area calc. off by more than 1e+6 km2"
    factor_surface = surface_area/surface_area[int(lat/2), int(lon/2)]
    if chatty:
        print('Grid resolution is {0}x{1}'.format(pixlon, pixlat))
        print('Calculated area is {0:3.1e} km2 (actual is 5.1e+8 km2)'.format(total_area))       
        print('Center pixel {0:4.3e} km2, weight {1:3.2f}'.format(surface_area[int(lat/2),0], factor_surface[int(lat/2),0]))
        print('Edge pixel {0:4.3e} km2, weight {1:3.2f}'.format(surface_area[0,0],factor_surface[0,0]))
    return surface_area, factor_surface

    surface_area(lat=180, lon=360)