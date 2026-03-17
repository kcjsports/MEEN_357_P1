from scipy.interpolate import interp1d
import subfunctions as sf
import matplotlib.pyplot as plt
import numpy as np
from define_experiment import experiment1 as ex1

effcy_tau = sf.Marvin["rover"]["wheel_assembly"]["motor"]["effcy_tau"]
effcy = sf.Marvin["rover"]["wheel_assembly"]["motor"]["effcy"]

effcy_fun = interp1d(effcy_tau, effcy, kind = 'cubic') # fit the cubic spline

x = np.linspace(effcy_tau.min(), effcy_tau.max(), 100)
y = effcy_fun(x)*100

plt.plot(x,y)
plt.plot(effcy_tau, effcy*100, marker = "*")
plt.xlabel('Torque (N-m)')
plt.ylabel('efficiency (%)')
plt.title('Vizualization of the Experiment Terrain')
plt.show()