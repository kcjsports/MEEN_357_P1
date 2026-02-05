import numpy as np

#what I think the dictionary if defined. IDK though.
Marvin = {
  #contains dictionarys about our rover
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

#checks

  if not (isinstance(omega, np.ndarray) or isinstance(motor, dict)):
    raise Exception("Inputs are not the right data type.")
  
  for i in range(len(omega)-1):
   if omega[i] 


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

