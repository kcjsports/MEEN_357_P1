import numpy as np

#what I think the dictionary is supposed to be. IDK though.
Marvin = {
  #contains dictionarys about the rover
    "rover" : {
        #contains definition about the rovers wheels inculuding details of what drives them
        "wheel_assembly" : {
          "wheel" : {"radius": 0.3 , "mass": 1.0}, #radius - m, mass - kg
          "speed_reducer" : {"typ": "good", "diam_pinion": 0.04, "diam_gear": 0.07, "mass":1.5}, 
          "motor": {"torque_stall": 170, "torque_noload": 0, "speed_noload": 3.80, "mass": 5.0},
        },
  #define the mass of the chassis of our rover
        "chassis": {"mass": 659},
  #define the mass of the chassis
        "science_payload" : {"mass": 75},
  #define the mass of the chassis
        "power_subsys": {"mass": 90},
    },
}

def taudc_motor(omega:np.ndarray, motor:dict):
  """
  Docstring for taudc_motor
  
  :param omega: An array of shaft speeds
  :type omega: np.ndarray
  :param motor: contains important 
  :type motor: dict
  """

  '''Returns the motor shaft torque in (Nm) given shaft speed, omeaga, in (rad/s)'''

#validates that the inputs are the correct data type
  if not (isinstance(omega, np.ndarray) or isinstance(motor, dict)):
    raise Exception("Inputs are not the right data type.")


#calculates the value of the tau
  tau = np.zeros(omega.size)
  for i in range(len(omega)):
    print(i)
    if omega[i] > motor["speed_noload"]: # for case where omega > omega_nl
      tau[i] = 0
    elif omega[i] < 0: # for case where omega < 0
      tau[i] = motor["torque_stall"] 
    else: # for case where 0 <= omega < omega_nl
      tau[i] = motor['torque_stall'] - ((motor['torque_stall']-motor['torque_noload'])/motor['speed_noload'])*omega[i]

  return tau

def get_gear_ratio(speed_reducer: dict):
  return Ng

def get_mass(rover: dict):
  return m

def F_drive(omega: np.ndarray, rover: dict):
  return Fd

def F_gravity(terrain_angle: np.ndarray, rover: dict, planet: dict):
  return Fgt

def F_rolling(omega: np.ndarray, terrain_angle: np.ndarray, rover: dict, planet: dict, Crr):
  return Frr

def F_net(omega: np.ndarray, terrain_angle: np.ndarray, rover: dict, planet: dict, Crr):
  return Fnet

