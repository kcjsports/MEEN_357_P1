import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
import subfunctions as sf

def f(o, ta, r, p, Crr = 0.15):
    return sf.F_net(np.array([o]), np.array([ta]), r, p, Crr)

#Imported variables
motor = sf.Marvin["rover"]["wheel_assembly"]["motor"]
rover = sf.Marvin["rover"]
planet = sf.Marvin["planet"]
#variables
omega = np.linspace(0, motor["speed_noload"], 25) #array of our omega 
Crr = 0.15
slope_array_deg = np.linspace(-15,35,25)
v_max = np.ndarray(25)
wheel_radius = sf.Marvin["rover"]["wheel_assembly"]["wheel"]["radius"]
motor = sf.Marvin["rover"]["wheel_assembly"]["motor"]

#Find where Fnet - tau/r = 0 for all values in slope array
root = np.zeros(25)
for i in range(25):
    root[i] = root_scalar(f,method='bisect', args=(slope_array_deg[i],rover, planet), bracket=[0,motor['speed_noload']]).root
print(root)


# plt.plot(slope_array_deg, v_max)
# plt.xlabel('Terrain Angle (degrees)')
# plt.ylabel('Maximum Rover Velocity (m/s)')
# plt.title('Rover Maximum Velocity vs Terrain Slope')
# plt.show()