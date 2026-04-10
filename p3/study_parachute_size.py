import numpy as np
import matplotlib.pyplot as plt
from define_edl_system import *
from subfunctions_EDL import *
from define_planet import *
from define_mission_events import *
from redefine_edl_system import *

# *************************************
# load dicts that define the EDL system (includes rover), planet,
# mission events and so forth.
edl_system = define_edl_system_1()
mars = define_planet()
mission_events = define_mission_events()


para_dia = np.linspace(14,19,11) #[m] the parachute diameters we are interested in
tmax = 2000   # [s] maximum simulated time



t_term = np.zeros(para_dia.size)
v_touchdown_term = np.zeros(para_dia.size)
rover_success = np.zeros(para_dia.size)
for i in range(para_dia.size):
    redefine_edl_system(edl_system)
    edl_system['altitude'] = 11000    # [m] initial altitude
    edl_system['velocity'] = -590     # [m/s] initial velocity
    edl_system['parachute']['deployed'] = True # our parachute is open
    edl_system['parachute']['ejected'] = False # and still attached
    edl_system['parachute']['ideal'] = True
    edl_system['rover']['on_ground'] = False # the rover has not yet landed
    edl_system['parachute']['diameter'] = para_dia[i]
    [t, Y, edl_system] = simulate_edl(edl_system, mars, mission_events, tmax, False)
    t_term[i] = t[-1]
    v_touchdown_term[i] = abs(Y[0,-1] + Y[5,-1])
    if Y[1,-1] >= edl_system["sky_crane"]["danger_altitude"] and abs(Y[0,-1] + Y[5,-1]) <= abs(edl_system["sky_crane"]["danger_speed"]):
        rover_success[i] = 1
    else:
        rover_success[i] = 0

fig, axs = plt.subplots(3,1, figsize=(9,9))

axs[0].plot(para_dia, t_term)
axs[0].set_title('parachute diameter vs. total time to land', fontsize=10)
axs[0].grid()
axs[1].plot(para_dia, v_touchdown_term)
axs[1].set_title('parachute diameter vs. touchdown speed of the rover', fontsize=10)
axs[1].grid()
axs[2].plot(para_dia,rover_success)
axs[2].set_title('parachute diameter vs. landing succees', fontsize=10)
axs[2].grid()

axs[0].set_xlabel('Diameter (m)')
axs[1].set_xlabel('Diameter (m)')
axs[2].set_xlabel('Diameter (m)')

axs[0].set_ylabel('Time to land (s)')
axs[1].set_ylabel('Touchdown Speed (m/s)')
axs[2].set_ylabel('Succees')
plt.tight_layout()
plt.show()