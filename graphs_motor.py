import matplotlib.pyplot as plt
import numpy as np
from subfunctions import tau_dcmotor, Marvin

motor = Marvin["rover"]["wheel_assembly"]["motor"]
N = 25 #our number of data point
omega = np.linspace(0, motor["speed_noload"], N) #array of our omega 

t = tau_dcmotor(omega,motor) #calulates the value of our tau values

#defines and calulates power at each omega
p = np.ndarray(N)
for i in  range(len(omega)):
  p[i] = t[i]*omega[i]


plt.rcParams["font.family"] = "serif"

fig, axes = plt.subplots(3,1, figsize=(9,9))

axes[0].plot(t, omega); axes[0].set_title("Motor - Torque vs. Speed")
axes[1].plot(t, p); axes[1].set_title("Motor - Torque vs. Power")
axes[2].plot(omega, p); axes[2].set_title("Motor - Speed vs. Power")

axes[0].set_xlabel('Torque')
axes[1].set_xlabel('Torque')
axes[2].set_xlabel('Speed')

axes[0].set_ylabel('Speed')
axes[1].set_ylabel('Power')
axes[2].set_ylabel('Power')


axes[0].set_box_aspect(1)
axes[1].set_box_aspect(1)
axes[2].set_box_aspect(1)

fig.tight_layout()

plt.show()