import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
import subfunctions as sf
from subfunctions import Marvin

#function that gets fed to the root finder
def f(o, ta, r, p, Crr = 0.15):
    result = sf.F_net(o, ta, r, p, Crr)
    return result

#Imported variables
motor = Marvin["rover"]["wheel_assembly"]["motor"]
rover = Marvin["rover"]
planet = Marvin["planet"]
wheel_radius = Marvin["rover"]["wheel_assembly"]["wheel"]["radius"]

#variables
omega = np.linspace(0, motor['speed_noload'], 25) #array of our omega 
Crr_array = np.linspace(0.01,0.5,25)
slope_array_deg = np.zeros(25)
v_max = np.ndarray(25)


#finds v_max at each slope
for i in range(25):
    if f(0, 0,rover, planet, Crr_array[i]) * f(3.8, 0,rover, planet, Crr_array[i]) >= 0:
        v_max[i] = motor['speed_noload'] * wheel_radius
    else:
        v_max[i] = root_scalar(f,method='bisect', args=(slope_array_deg[i],rover, planet,Crr_array[i]), bracket=[0,motor['speed_noload']]).root * wheel_radius


plt.plot(Crr_array, v_max)
plt.xlabel('Coefficient of Rolling Resistance')
plt.ylabel('Maximum Rover Velocity (m/s)')
plt.title('Rover Maximum Velocity at different Coefficient of Rolling Resistance')
plt.show()