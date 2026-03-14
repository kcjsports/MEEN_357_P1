from scipy.interpolate import interp1d
import subfunctions as sf
import matplotlib.pyplot as plt
import numpy as np

#original data points
alpha_dist = sf.Marvin["experiment"]['alpha_dist']
alpha_deg = sf.Marvin["experiment"]['alpha_deg']

#original data interpolated between useing an cubic spline
alpha_fun = interp1d(alpha_dist, alpha_deg, kind = 'cubic', fill_value='extrapolate') #fit the cubic spline

#
x = np.linspace(alpha_dist.min(), alpha_dist.max(), 100)
y = alpha_fun(x)

plt.plot(x,y)
plt.plot(alpha_dist,alpha_deg, marker = "*")
plt.xlabel('Position (m)')
plt.ylabel('Terrain Angle (degrees)')
plt.title('Vizualization of the Experiment Terrain')
plt.show()