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

#Array Telemetry

for time in experiment["time_range"]:
  pos, vel = sf.simulate_rover(rover,planet,experiment,end_event)
  telemetry["position"] = np.append(telemetry["position"], pos)
  telemetry["velocity"] = np.append(telemetry["velocity"], vel)
  telemetry["Power"] = np.append(telemetry["Power"], 6 * sf.mechpower(telemetry["velocity"][-1], rover))
  telemetry["time"] = np.append(telemetry["time"], time)
  if time > end_event["max_time"] or telemetry["position"][-1] > end_event["max_distance"] or telemetry["velocity"][-1] < end_event["min_velocity"]:
    break

#Non-array Telemetry

telemetry["distance_traveled"] = telemetry["position"][-1]
telemetry["max_velocity"] = np.max(telemetry["velocity"])
telemetry["average_velocity"] = telemetry["distance_traveled"] / telemetry["time"][-1]
telemetry["battery_energy"] = sf.battenergy(telemetry["time"],telemetry["velocity"], rover):
telemetry["energy_per_distance"] = telemetry["battery_energy"] / telemetry["distance_traveled"]
telemetry["completition_time"] = telemetry["time"][-1]

#Graphs 

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
