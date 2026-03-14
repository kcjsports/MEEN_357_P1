import numpy as np
from scipy.optimize import root_scalar
import matplotlib.pyplot as plt
import subfunctions as sf
from mpl_toolkits.mplot3d import Axes3D

#function that gets fed to the root finder
def f(o, ta, r, p, Crr):
    return sf.F_net(np.array([o]), np.array([ta]), r, p, Crr)

#Imported variables
motor = sf.Marvin["rover"]["wheel_assembly"]["motor"]
rover = sf.Marvin["rover"]
planet = sf.Marvin["planet"]
wheel_radius = sf.Marvin["rover"]["wheel_assembly"]["wheel"]["radius"]
#variables
Crr_array = np.linspace(0.01,0.5,25)
slope_array_deg = np.linspace(-15,35,25)
CRR, SLOPE = np.meshgrid(Crr_array, slope_array_deg)
VMAX = np.zeros(np.shape(CRR), dtype = float)

#finds v_max at each slope
N = np.shape(CRR)[0]
for i in range(N):
 for j in range(N):
    Crr_sample = float(CRR[i,j])
    slope_sample = float(SLOPE[i,j])
    if f(0, slope_array_deg[i],rover, planet, Crr_array[j]) * f(3.8, slope_array_deg[i],rover, planet, Crr_array[j]) >= 0:
       VMAX[i,j] = float('NaN')
    else:
       VMAX[i,j] = root_scalar(f,method='bisect', args=(slope_array_deg[i],rover, planet, Crr_array[j]), bracket=[0,motor['speed_noload']]).root * wheel_radius


figure = plt.figure()
ax = figure.add_subplot(projection='3d')
ax.plot_surface(CRR, SLOPE, VMAX)
ax.view_init(27, -10)
ax.set_xlabel("Coefficent of rolling resistance")
ax.set_ylabel('Terrain Angle')
ax.set_zlabel('Max Velocity (m/s)')
plt.title('Maximum Velocity at Different \n Terrain Angles and Coefficent of Rolling Resistance')
plt.show()