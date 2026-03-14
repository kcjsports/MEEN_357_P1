import numpy as np
import numbers
from math import erf

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

def tau_dcmotor(omega: np.ndarray, motor:dict):
  """_summary_

  Args:
      omega (np.ndarray): _description_
      motor (dict): _description_

  Raises:
      Exception: _description_
      Exception: _description_

  Returns:
      _type_: _description_
      
  """

#validates that the inputs are the correct data type
  if not isinstance(omega, np.ndarray):
    raise Exception("input speed should be a scalar or array")
  if not isinstance(motor, dict):
    raise Exception("Arg 2 should be dict")
#calculates the value of the tau
  tau = np.zeros(omega.size)
  for i in range(omega.size):
    if omega[i] > motor["speed_noload"]: # for case where omega > omega_nl
      tau[i] = 0
    elif omega[i] < 0: # for case where omega < 0
      tau[i] = motor["torque_stall"] 
    else: # for case where 0 <= omega < omega_nl
      tau[i] = motor['torque_stall'] - ((motor['torque_stall']-motor['torque_noload'])/motor['speed_noload'])*omega[i]
  return tau

def get_gear_ratio(speed_reducer: dict):
  """_summary_

  Args:
      speed_reducer (dict): _description_

  Raises:
      Exception: _description_
      Exception: _description_
      Exception: _description_

  Returns:
      _type_: _description_
  """
  if not isinstance(speed_reducer, dict):
        raise Exception("Expected speed_reducer to be a dictionary.")
  if "type" not in speed_reducer:
        raise Exception("speed_reducer must contain a 'type' field.")
  if speed_reducer["type"].lower() != "reverted":
        raise Exception("Error: expected speed reducer type 'reverted'.")
  Ng = (speed_reducer["diam_gear"] / speed_reducer["diam_pinion"]) ** 2
  return Ng

def get_mass(rover: dict):
  """_summary_

  Args:
      rover (dict): _description_

  Raises:
      Exception: _description_

  Returns:
      _type_: _description_
  """
  if not isinstance(rover, dict):
        raise Exception("Expected rover to be a dictionary.")
  m_chassis = rover["chassis"]["mass"]
  m_science = rover["science_payload"]["mass"]
  m_power = rover["power_subsys"]["mass"]
  m_motor = rover["wheel_assembly"]["motor"]["mass"]
  m_speed_reducer = rover["wheel_assembly"]["speed_reducer"]["mass"]
  m_wheel = rover["wheel_assembly"]["wheel"]["mass"]
  m =  m_chassis + m_science + m_power + 6 * (m_motor + m_speed_reducer + m_wheel)
  return m

def F_drive(omega: np.ndarray, rover: dict):
  """_summary_

  Args:
      omega (np.ndarray): _description_
      rover (dict): _description_

  Raises:
      Exception: _description_
      Exception: _description_

  Returns:
      _type_: _description_
  """
  if not isinstance(omega, np.ndarray):
    raise Exception("input speed should be a scalar or array")
  if not isinstance(rover, dict):
    raise Exception("Arg 2 should be dict")
  Ng = get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])
  tau = tau_dcmotor(omega, rover["wheel_assembly"]["motor"])
  Fd = 6 * Ng * tau / rover["wheel_assembly"]["wheel"]["radius"] #6 wheels * gear_ratio * shaft torque / radius of the wheel
  return Fd

def F_gravity(terrain_angle: np.ndarray, rover: dict, planet: dict):
  """_summary_

  Args:
      terrain_angle (np.ndarray): _description_
      rover (dict): _description_
      planet (dict): _description_

  Raises:
      Exception: _description_
      Exception: _description_

  Returns:
      _type_: _description_
  """
  #input validation
  if not isinstance(terrain_angle, np.ndarray) and not isinstance(rover, dict) or not isinstance(planet, dict):
    raise Exception("Inputs are not the right data type.")
  if min(terrain_angle) < -75 or max(terrain_angle) > 75:
     raise Exception("To steep")
  
  #calculates the force of gravity
  Fgt = np.zeros(terrain_angle.size)
  m = get_mass(rover)
  for i in range(len(terrain_angle)):
    Fgt[i] = -1 * m * planet["g"] * np.sin(np.radians(terrain_angle[i]))
  return Fgt

def F_rolling(omega: np.ndarray, terrain_angle: np.ndarray, rover: dict, planet: dict, Crr):
  """_summary_

  Args:
      omega (np.ndarray): _description_
      terrain_angle (np.ndarray): _description_
      rover (dict): _description_
      planet (dict): _description_
      Crr (_type_): _description_

  Raises:
      Exception: _description_
      Exception: _description_
      Exception: _description_
      Exception: _description_
      Exception: _description_

  Returns:
      _type_: _description_
  """
  #input validation
  if not isinstance(omega, np.ndarray) or not isinstance(terrain_angle, np.ndarray):
     raise Exception("Args 1/2 should be np.ndarray.")
  if not isinstance(rover, dict) or not isinstance(planet, dict):
      raise Exception("Args 3/4 should be dicts.")
  if Crr < 0:
    raise Exception("Crr must be a postive scalar")
  if omega.size != terrain_angle.size:
     raise Exception("omega and terrain_angle arrays must be the same size")
  if min(terrain_angle) < -75 or max(terrain_angle) > 75:
     raise Exception("To steep")
  
  #calculates the rolling force
  m = get_mass(rover)
  Ng = get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])
  Frr = np.zeros(omega.size)
  for i in range(omega.size):
    Fn = m * planet["g"] * np.cos(np.radians(terrain_angle[i]))
    Frr_simple = -Crr * Fn
    Frr[i] =  erf(40 * (omega[i] / Ng) * rover["wheel_assembly"]["wheel"]["radius"]) * Frr_simple
  return Frr


def F_net(omega: np.ndarray, terrain_angle: np.ndarray, rover: dict, planet: dict, Crr: float):
  """_summary_

  Args:
      omega (np.ndarray): _description_
      terrain_angle (np.ndarray): _description_
      rover (dict): _description_
      planet (dict): _description_
      Crr (float): _description_

  Raises:
      Exception: _description_
      Exception: _description_
      Exception: _description_
      Exception: _description_
      Exception: _description_

  Returns:
      _type_: _description_
  """
  if not isinstance(omega, np.ndarray) or not isinstance(terrain_angle, np.ndarray):
     raise Exception("Args 1/2 should be np.ndarray.")
  if not isinstance(rover, dict) or not isinstance(planet, dict):
      raise Exception("Args 3/4 should be dicts.")
  if Crr <= 0:
    raise Exception("Your Crr input must be a postive input")
  if omega.size != terrain_angle.size:
     raise Exception("omega and terrain_angle must be equivalent length")
  minu = np.min(terrain_angle)
  maxu = np.max(terrain_angle)
  if minu < -75 or maxu > 75:
     raise Exception("To steep")
  Fd = F_drive(omega, rover)
  Fgt = F_gravity(terrain_angle, rover, planet)
  Frr = F_rolling(omega, terrain_angle, rover, planet, Crr)
  Fnet = Fd + Fgt + Frr
  return Fnet

def motorW(v: np.ndarray, rover: dict):
  """_summary_

  Args:
      v (np.ndarray): _description_
      rover (dict): _description_

  Raises:
      Exception: _description_
      Exception: _description_
      Exception: _description_

  Returns:
      _type_: _description_
  """
   #input validation
  if not isinstance(v, (np.ndarray, numbers.Number)):
      raise Exception("The rotaional velocity of the rover must be in the form of a scalar or a vector")
  if isinstance(v, np.ndarray) and not v.ndim == 1:
      raise Exception("The rotaional velocity vector must only have one row")
  if not isinstance(rover, dict):
      raise Exception("The rover input must be a dictonary")
  
   #caluates and returns the rotional speed of the shaft
  r = rover["wheel_assembly"]["wheel"]["radius"] #radius of the wheels
  w_out = v/r #W_out is the roational speed of the wheels
  w_in = w_out * get_gear_ratio(rover["wheel_assembly"]["speed_reducer"]) #W_out is the roational speed of the shaft
  return w_in 


def rover_dynamics(t: float, y: np.ndarray, rover: dict, planet: dict, experiment: dict):
  
   return dydt

def mechpower(v: np.ndarray, rover: dict):
   
   return P

def battenergy(t: np.ndarray, v: np.ndarray, rover: dict):
   
   return E

def simulate_rover(rover: dict, planet: dict, experiment: dict, end_event: dict):
   
   return rover