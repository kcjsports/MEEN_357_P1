import numpy as np

Marvin = {
  #contains dictionarys about the rover
    "rover" : {
        "wheel_assembly" : { #contains definition about the rovers wheels inculuding details of what drives them
          "wheel" : {"radius" : 0.3 , "mass" : 1.0}, #radius - m, mass - kg
          "speed_reducer" : {"type" : "reverted", "diam_pinion" : 0.04, "diam_gear" : 0.07, "mass" : 1.5}, 
          "motor": {"torque_stall" : 170, "torque_noload" : 0, "speed_noload" : 3.80, "mass" : 5.0, "effcy_tau" : np.array([0, 10, 20, 40, 70, 165]), "effcy" : np.array([0, 0.60, 0.78, 0.73, 0.53, 0.04])},
          "telemetry" : {"time" : 0, "completition_time" : 0, "velocity" : 0, "position": 0, "distance_traveled": 0, "max_velocity": 0, "average_velocity": 0, "Power": 0, "battery_energy": 0, "energy_per_distance": 0}
        },
        "chassis": {"mass" : 659},   #define the mass of the chassis of our rover
        "science_payload" : {"mass" : 75},   #define the mass of the chassis
        "power_subsys" : {"mass" : 90},   #define the mass of the chassis
    },
    "planet" : {"g" : 3.72},
    "experiment" : {'time_range' : np.array([0,20000]), 'initial_conditions' : np.array([0.325,0]), 'alpha_dist' : np.array([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]), 'alpha_deg' : np.array([2.032, 11.509, 2.478, 7.182, 5.511, 10.981, 5.601, -0.184, 0.714, 4.151, 4.042]), 'Crr' : 0.1},
    "end_event" : {"max_distance" : 50, "max_time" : 5000, "max_velocity" : 0.01}
}