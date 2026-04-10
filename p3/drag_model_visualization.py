import numpy as np
import matplotlib.pyplot as plt
from define_edl_system import *
from scipy.interpolate import interp1d

m_data = np.array([0.25, 0.5, 0.65, 0.70, 0.8, 0.9, 0.95, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2.0, 2.2, 2.5, 2.6])
MEF_data = np.array([1,1,1, 0.97, 0.91, 0.72, 0.66, 0.75, 0.9, 0.96, 0.99, 0.999, 0.992, 0.98, 0.91, 0.85, 0.82, 0.75, 0.64, 0.62])
plt.scatter(m_data,MEF_data)
plt.xlabel('MACH')
plt.ylabel('MEF')
plt.title('Vizualization of Mach MEF relation')
plt.grid()

x = np.linspace(m_data.min(), m_data.max(), num=100)

get_MEF = interp1d(m_data, MEF_data, kind='cubic')
plt.plot(x, get_MEF(x))

plt.show()