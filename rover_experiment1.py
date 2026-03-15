import numpy as np
import matplotlib.pyplot as plt
from subfunctions import Marvin
import subfunctions as sf
from define_experiment import define_experiment
from end_of_mission_event import end_of_mission_event


#Imported variables
rover = Marvin["rover"]
planet = Marvin["planet"]
experiment, end_event = define_experiment()
events = end_of_mission_event(end_event)

pos = np.ndarray()
vel = np.ndarray()
acel = np.ndarray()
for time in experiment["time_range"]:
  rover["telemetry"] = sf.simulate_rover(rover,planet,experiment,end_event)
  pos = np.append(pos, rover["telemetry"]["position"])
  vel = np.append(vel, rover["telemetry"]["velocity"])
  acel = np.append(acel, rover["telemetry"]["acceleration"])


plt.rcParams["font.family"] = "serif"

fig, axes = plt.subplots(3,1, figsize=(9,9))

axes[0].plot(experiment["time_range"], pos); axes[0].set_title("Motor - Torque vs. Speed (Without Speed Reducer)")
axes[1].plot(experiment["time_range"], vel); axes[1].set_title("Motor - Torque vs. Power (Without Speed Reducer)")
axes[2].plot(experiment["time_range"], acel); axes[2].set_title("Motor - Speed vs. Power (Without Speed Reducer)")

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
