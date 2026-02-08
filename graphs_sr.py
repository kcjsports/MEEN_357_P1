import matplotlib.pyplot as plt
import numpy as np
import subfunctions
import graphs_motor

Marvin = subfunctions.Marvin
motor = Marvin["rover"]["wheel_assembly"]["motor"]
N = graphs_motor.N #our number of data point
omega = np.linspace(0, motor["speed_noload"], N) #array of our omega
t = subfunctions.taudc_motor(omega,motor) #calulates the value of our tau values
Ng = subfunctions.get_gear_ratio(Marvin["rover"]["wheel_assembly"]["speed_reducer"])
omega_out = omega / Ng
tau_out = t * Ng

#defines and calulates power at each omega
p = np.ndarray(N)
for i in  range(len(omega_out)):
  p[i] = tau_out[i]*omega_out[i]


plt.rcParams["font.family"] = "serif"
fig, ax = plt.subplots(3,1)
ax[0].plot(tau_out, omega_out); ax[0].set_title("Motor - Torque vs. Speed")
ax[1].plot(tau_out, p); ax[1].set_title("Motor - Torque vs. Power")
ax[2].plot(omega_out, p); ax[2].set_title("Motor - Speed vs. Power")


plt.show()