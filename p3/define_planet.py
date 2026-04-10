"""###########################################################################
#   This file contains planet dict definitions
#
#   Created by: Former Marvin Numerical Methods Engineering Team
#   Last Modified: 22 October 2021
###########################################################################"""

import numpy as np

def define_planet():

    high_altitude = {'temperature' : lambda altitude: -23.4 - 0.00222*altitude, # [C] Temperature calculation at high altitudes on Mars
                     'pressure' : lambda altitude: 0.699*np.exp(-0.00009*altitude)} # [KPa] Pressure calculation at high altitudes on Mars
                                                                
    low_altitude = {'temperature' : lambda altitude: -31 - 0.000998*altitude, # [C] Temperature calculation at low altitudes on Mars
                    'pressure' : lambda altitude: 0.699*np.exp(-0.00009*altitude)} # [KPa] Pressure calculation at low altitudes on Mars
    
    density = lambda temperature, pressure: pressure/(0.1921*(temperature+273.15)) # [kg/m^3]
    
    mars = {'g' : -3.72,   # m/s^2] # Gravity on Mars
            'altitude_threshold' : 7000, # [m] High/low altitude crossover
            'low_altitude' : low_altitude, # See low_altitude
            'high_altitude' : high_altitude, # See high_altitude
            'density' : density} # Air density on mars
    
    #del high_altitude, low_altitude, density
    return mars
                                                            