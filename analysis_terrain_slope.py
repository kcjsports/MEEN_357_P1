import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
import subfunctions
import graphs_motor


#Imported variables
N = graphs_motor.N #our number of data point
Marvin = subfunctions.Marvin
omega = graphs_motor.omega

#variables
Crr = 0.15
slope_array_deg = np.linspace(-15,35,N)
v_max = np.ndarray(N)
wheel_radius = Marvin["rover"]["wheel_assembly"]["wheel"]["radius"]


#Find where Fnet - tau/r = 0 for all values in slope array



plt.plot(slope_array_deg, v_max)
plt.xlabel('Terrain Angle (degrees)')
plt.ylabel('Maximum Rover Velocity (m/s)')
plt.title('Rover Maximum Velocity vs Terrain Slope')
plt.show()