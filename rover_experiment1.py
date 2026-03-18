import numpy as np
import matplotlib.pyplot as plt
from subfunctions import Marvin
import subfunctions as sf
from define_experiment import experiment1
from end_of_mission_event import end_of_mission_event


#Imported variables
rover = Marvin["rover"]
planet = Marvin["planet"]
telemetry = rover["telemetry"]
experiment, end_event = experiment1()
events = end_of_mission_event(end_event)

rover = sf.simulate_rover(rover, planet, experiment, end_event)

#Graphs 

plt.rcParams["font.family"] = "serif"

fig, axes = plt.subplots(3,1, figsize=(9,9))

axes[0].plot(experiment["time_range"], telemetry["Position"]); axes[0].set_title("Motor - Torque vs. Speed (Without Speed Reducer)")
axes[1].plot(experiment["time_range"], telemetry["Velocity"]); axes[1].set_title("Motor - Torque vs. Power (Without Speed Reducer)")
axes[2].plot(experiment["time_range"], telemetry["Power"]); axes[2].set_title("Motor - Speed vs. Power (Without Speed Reducer)")

axes[0].set_xlabel('Time (s)')
axes[1].set_xlabel('Time (s)')
axes[2].set_xlabel('Time (s)')

axes[0].set_ylabel('Position (m)')
axes[1].set_ylabel('Velocity (m/s)')
axes[2].set_ylabel('Acceleration (m/s^2)')


axes[0].set_box_aspect(1)
axes[1].set_box_aspect(1)
axes[2].set_box_aspect(1)

fig.tight_layout()

plt.show()
