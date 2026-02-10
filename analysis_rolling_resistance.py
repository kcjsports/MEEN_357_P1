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
Crr_array = np.linspace(0.01,0.5,25)
slope_array_deg = np.zeros(25)
v_max = np.ndarray(25)
wheel_radius = sf.Marvin["rover"]["wheel_assembly"]["wheel"]["radius"]

#finds v_max at each slope
for i in range(25):
    if f(0, 0,rover, planet, Crr_array[i]) * f(3.8, 0,rover, planet, Crr_array[i]) >= 0:
        v_max[i] = motor['speed_noload'] * wheel_radius
    else:
        v_max[i] = root_scalar(f,method='bisect', args=(slope_array_deg[i],rover, planet,Crr_array[i]), bracket=[0,motor['speed_noload']]).root * wheel_radius


plt.plot(Crr_array, v_max)
plt.xlabel('Coefficient of Rolling Resistance')
plt.ylabel('Maximum Rover Velocity (m/s)')
plt.title('Rover Maximum Velocity vs Coefficient of Rolling Resistance')
plt.show()