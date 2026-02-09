import matplotlib.pyplot as plt
import numpy as np
from subfunctions import tau_dcmotor, get_gear_ratio, Marvin

motor = Marvin["rover"]["wheel_assembly"]["motor"]
N = 25 #our number of data point
omega = np.linspace(0, motor["speed_noload"], N) #array of our omega 

t = tau_dcmotor(omega,motor) #calulates the value of our tau values

Ng = get_gear_ratio(Marvin["rover"]["wheel_assembly"]["speed_reducer"])

omega_out = np.zeros(N)
t_out = np.zeros(N)
for i in range(N):
  omega_out[i] = omega[i]/Ng
  t_out[i] = t[i] * Ng

#defines and calulates power at each omega
p = np.ndarray(N)
for i in  range(len(omega_out)):
  p[i] = t_out[i]*omega_out[i]


plt.rcParams["font.family"] = "serif"

fig, axes = plt.subplots(3,1, figsize=(9,9))

axes[0].plot(t_out, omega_out); axes[0].set_title("Motor - Torque vs. Speed")
axes[1].plot(t_out, p); axes[1].set_title("Motor - Torque vs. Power")
axes[2].plot(omega_out, p); axes[2].set_title("Motor - Speed vs. Power")

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