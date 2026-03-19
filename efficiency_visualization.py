from scipy.interpolate import interp1d
import subfunctions as sf
import matplotlib.pyplot as plt
import numpy as np

#given tau and the efficincy at those tau's
effcy_tau = sf.Marvin["rover"]["wheel_assembly"]["motor"]["effcy_tau"]
effcy = sf.Marvin["rover"]["wheel_assembly"]["motor"]["effcy"]

#uses a cubic spline to interpolate tau and efficincy data
effcy_fun = interp1d(effcy_tau, effcy, kind = 'cubic') # fit the cubic spline

#dfines data
x = np.linspace(effcy_tau.min(), effcy_tau.max(), 100)
y = effcy_fun(x)*100

#plots data
plt.plot(x,y)
plt.plot(effcy_tau, effcy*100, marker = "*")
plt.xlabel('Torque (N-m)')
plt.ylabel('Efficiency (%)')
plt.title('Efficiency of the DC Motor')
plt.show()