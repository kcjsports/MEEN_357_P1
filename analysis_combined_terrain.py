import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
import graphs_motor
import subfunctions

#imported variables
N = graphs_motor.N #our number of data point
Marvin = subfunctions.Marvin
omega = graphs_motor.omega

#variables
Crr_array = np.linspace(0.01,0.5,N)
slope_array_deg = np.linspace(-15,35,N)
CRR, SLOPE = np.meshgrid(Crr_array, slope_array_deg)
VMAX = np.zeros(np.shape(CRR), dtype=float)



M = np.shape(CRR)[0]
for i in range(N):
  for j in range(N):
    Crr_sample = float(CRR[i,j])
    slope_sample = float(SLOPE[i,j])
    VMAX[i,j] = 


