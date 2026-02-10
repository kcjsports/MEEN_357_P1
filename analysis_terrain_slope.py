import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
import subfunctions as sf

#function that gets fed to the root finder
def f(o, ta, r, p, Crr = 0.15):
    return sf.F_net(np.array([o]), np.array([ta]), r, p, Crr)

#Imported variables
motor = sf.Marvin["rover"]["wheel_assembly"]["motor"]
rover = sf.Marvin["rover"]
planet = sf.Marvin["planet"]
#variables
omega = np.linspace(0, motor['speed_noload'], 25) #array of our omega 
Crr = 0.15
slope_array_deg = np.linspace(-15,35,25)
v_max = np.ndarray(25)
wheel_radius = sf.Marvin["rover"]["wheel_assembly"]["wheel"]["radius"]

#finds v_max at each slope
for i in range(25):
    if f(0, slope_array_deg[i],rover, planet) * f(3.8, slope_array_deg[i],rover, planet) >= 0:
        v_max[i] = float('NaN')
    else:
        v_max[i] = root_scalar(f,method='bisect', args=(slope_array_deg[i],rover, planet), bracket=[0,motor['speed_noload']]).root * wheel_radius


plt.plot(slope_array_deg, v_max)
plt.xlabel('Terrain Angle (degrees)')
plt.ylabel('Maximum Rover Velocity (m/s)')
plt.title('Rover Maximum Velocity at Different Terrain Angles')
plt.show()