import matplotlib.pyplot as plt
import numpy as np
from subfunctions import taudc_motor, Marvin

m = Marvin["rover"]["wheel_assembly"]["motor"]
n = 39 #our number of data point
o = np.linspace(0, m["speed_noload"], n) #array of our omega 

t = taudc_motor(o,m) #calulates the value of our tau values

#defines and calulates power at each omega
p = np.ndarray(n)
for i in  range(len(o)):
  p[i] = t[i]*o[i]


plt.rcParams["font.family"] = "serif"
fig, ax = plt.subplots(3,1)
ax[0].plot(t, o); ax[0].set_title("Motor - Torque vs. Speed")
ax[1].plot(t, p); ax[1].set_title("Motor - Torque vs. Power")
ax[2].plot(o, p); ax[2].set_title("Motor - Speed vs. Power")


plt.show()