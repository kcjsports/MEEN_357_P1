import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
import graphs_motor
import subfunctions

#Imported variables
N = graphs_motor.N #our number of data point
Marvin = subfunctions.Marvin
omega = graphs_motor.omega

#variables
Crr_array = np.linspace(0.01,0.5,25)
slope_array_deg = np.zeros(N)
v_max = np.ndarray(N)
wheel_radius = Marvin["rover"]["wheel_assembly"]["wheel"]["radius"]



#Find where Fnet - tau/r = 0 for all values in slope array




plt.plot(Crr_array, v_max)
plt.xlabel('Terrain Angle (degrees)')
plt.ylabel('Maximum Rover Velocity (m/s)')
plt.title('Rover Maximum Velocity vs Terrain Slope')
plt.show()
