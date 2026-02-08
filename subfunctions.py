import numpy as np
from scipy import special

Marvin = {
  #contains dictionarys about the rover
    "rover" : {
        "wheel_assembly" : { #contains definition about the rovers wheels inculuding details of what drives them
          "wheel" : {"radius" : 0.3 , "mass" : 1.0}, #radius - m, mass - kg
          "speed_reducer" : {"type" : "reverted", "diam_pinion" : 0.04, "diam_gear" : 0.07, "mass" : 1.5}, 
          "motor": {"torque_stall" : 170, "torque_noload" : 0, "speed_noload" : 3.80, "mass" : 5.0},
        },
        "chassis": {"mass" : 659},   #define the mass of the chassis of our rover
        "science_payload" : {"mass" : 75},   #define the mass of the chassis
        "power_subsys" : {"mass" : 90},   #define the mass of the chassis
    },
    "planet" : {"g_mars" : 3.72}
}

def tau_dcmotor(omega: np.ndarray, motor:dict):
  """
  Docstring for taudc_motor
  
  :param omega: An array of shaft speeds
  :type omega: np.ndarray
  :param motor: contains important 
  :type motor: dict
  """

  '''Returns the motor shaft torque in (Nm) given shaft speed, omeaga, in (rad/s)'''

#validates that the inputs are the correct data type
  if not isinstance(omega, np.ndarray) or not isinstance(motor, dict):
    raise Exception("Inputs are not the right data type.")
#calculates the value of the tau
  tau = np.zeros(omega.size)
  for i in range(len(omega)):
    if omega[i] > motor["speed_noload"]: # for case where omega > omega_nl
      tau[i] = 0
    elif omega[i] < 0: # for case where omega < 0
      tau[i] = motor["torque_stall"] 
    else: # for case where 0 <= omega < omega_nl
      tau[i] = motor['torque_stall'] - ((motor['torque_stall']-motor['torque_noload'])/motor['speed_noload'])*omega[i]
  return tau

def get_gear_ratio(speed_reducer: dict):
  if not isinstance(speed_reducer, dict):
        raise Exception("Expected speed_reducer to be a dictionary.")
  if "type" not in speed_reducer:
        raise Exception("speed_reducer must contain a 'type' field.")
  if speed_reducer["type"].lower() != "reverted":
        raise Exception("Error: expected speed reducer type 'reverted'.")
  Ng = (speed_reducer["diam_gear"] / speed_reducer["diam_pinion"]) ** 2
  return Ng

def get_mass(rover: dict):
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
  if not isinstance(omega, np.ndarray) or not isinstance(rover, dict):
    raise Exception("Inputs are not the right data type.")
  gear_ratio = get_gear_ratio(Marvin["rover"]["wheel_assembly"]["speed_reducer"])
  shaft_torque = taudc_motor(omega, Marvin["rover"]["wheel_assembly"]["motor"])
  Fd = 6 * omega * gear_ratio * shaft_torque #6 wheels * speed * gear_ratio * shaft torque
  return Fd

def F_gravity(terrain_angle: np.ndarray, rover: dict, planet: dict):
  if not isinstance(terrain_angle, np.ndarray) and not isinstance(rover, dict) or not isinstance(planet, dict):
    raise Exception("Inputs are not the right data type.")
  if min(terrain_angle) < -75 or max(terrain_angle) > 75:
     raise Exception("To steep")
  m = get_mass(Marvin["rover"])
  Fgt = m * planet["g_mars"] * np.sin(np.radians(terrain_angle))
  return Fgt

def F_rolling(omega: np.ndarray, terrain_angle: np.ndarray, rover: dict, planet: dict, Crr):
  if not isinstance(omega, np.ndarray) or not isinstance(terrain_angle, np.ndarray) or not isinstance(rover, dict) or not isinstance(planet, dict):
     raise Exception("Inputs are not the right data type.")
  if Crr < 0:
    raise Exception("Crr must be a postive scalar")
  if len(omega) != len(terrain_angle):
     raise Exception("omega and terrain_angle must be equivalent length")
  if min(terrain_angle) < -75 or max(terrain_angle) > 75:
     raise Exception("To steep")
  m = get_mass(Marvin["rover"])
  Ng = get_gear_ratio(Marvin["rover"]["wheel_assembly"]["speed_reducer"])
  Fn = m * planet["g_mars"] * np.cos(np.radians(terrain_angle))
  Frr_simple = Crr * Fn
  Frr = special.erf(40 * omega * Ng * rover["wheel_assembly"]["wheel"]["radius"]) * Frr_simple
  return Frr

def F_net(omega: np.ndarray, terrain_angle: np.ndarray, rover: dict, planet: dict, Crr):
  if not isinstance(omega, np.ndarray) or not isinstance(terrain_angle, np.ndarray) or not isinstance(rover, dict) or not isinstance(planet, dict):
     raise Exception("Inputs are not the right data type.")
  if Crr < 0:
    raise Exception("Crr must be a postive scalar")
  if len(omega) != len(terrain_angle):
     raise Exception("omega and terrain_angle must be equivalent length")
  if min(terrain_angle) < -75 or max(terrain_angle) > 75:
     raise Exception("To steep")
  Fd = F_drive(omega, Marvin["rover"])
  Fgt = F_gravity(terrain_angle, Marvin["rover"], Marvin["planet"])
  Frr = F_rolling(omega, terrain_angle, Marvin["rover"], Marvin["planet"], Crr)
  Fnet = Fd + Fgt - Frr
  return Fnet

