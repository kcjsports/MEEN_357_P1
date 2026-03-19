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

rover = sf.simulate_rover(rover, planet, experiment, events) #simulate the rover's motion and store the telemetry data in the rover structure
telemetry = rover["telemetry"]

#Graphs 

plt.rcParams["font.family"] = "serif"

fig, axes = plt.subplots(3,1, figsize=(9,9))

axes[0].plot(telemetry["time"], telemetry["position"]); axes[0].set_title("Time vs. Position")
axes[1].plot(telemetry["time"], telemetry["velocity"]); axes[1].set_title("Time vs. Velocity")
axes[2].plot(telemetry["time"], telemetry["power"]); axes[2].set_title("Time vs. Power")

axes[0].set_xlabel('Time (s)')
axes[1].set_xlabel('Time (s)')
axes[2].set_xlabel('Time (s)')

axes[0].set_ylabel('Position (m)')
axes[1].set_ylabel('Velocity (m/s)')
axes[2].set_ylabel('Power (W)')


axes[0].set_box_aspect(1)
axes[1].set_box_aspect(1)
axes[2].set_box_aspect(1)

fig.tight_layout()

plt.show()

# #Telemetry values at the end of the mission
# print(telemetry["completition_time"])
# print(telemetry["distance_traveled"])
# print(telemetry["max_velocity"])
# print(telemetry["average_velocity"])
# print(telemetry["battery_energy"])
# print(telemetry["batt_energy_per_distance"])
# if telemetry["battery_energy"] < 0.9072e6:
#   print("Yes, The LiPo works")
# else: print("No, The LiPo does not work")