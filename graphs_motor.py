import matplotlib.pyplot as plt
import numpy as np
from subfunctions import taudc_motor, Marvin

motor = Marvin["rover"]["wheel_assembly"]["motor"]
N = 25 #our number of data point
omega = np.linspace(0, motor["speed_noload"], N) #array of our omega 

t = taudc_motor(omega,motor) #calulates the value of our tau values

#defines and calulates power at each omega
p = np.ndarray(N)
for i in  range(len(omega)):
  p[i] = t[i]*omega[i]


plt.rcParams["font.family"] = "serif"
fig, ax = plt.subplots(3,1)
ax[0].plot(t, omega); ax[0].set_title("Motor - Torque vs. Speed")
ax[1].plot(t, p); ax[1].set_title("Motor - Torque vs. Power")
ax[2].plot(omega, p); ax[2].set_title("Motor - Speed vs. Power")


plt.show()