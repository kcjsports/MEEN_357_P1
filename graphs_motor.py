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

axes[0].plot(t, omega); axes[0].set_title("Motor - Torque vs. Speed (Without Speed Reducer)")
axes[1].plot(t, p); axes[1].set_title("Motor - Torque vs. Power (Without Speed Reducer)")
axes[2].plot(omega, p); axes[2].set_title("Motor - Speed vs. Power (Without Speed Reducer)")

axes[0].set_xlabel('Torque (Nm)')
axes[1].set_xlabel('Torque (Nm)')
axes[2].set_xlabel('Speed (m/s)')

axes[0].set_ylabel('Speed(m/s)')
axes[1].set_ylabel('Power (W)')
axes[2].set_ylabel('Power (W)')


axes[0].set_box_aspect(1)
axes[1].set_box_aspect(1)
axes[2].set_box_aspect(1)

fig.tight_layout()

plt.show()