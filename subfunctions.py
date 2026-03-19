import numpy as np
import numbers
from math import erf
import scipy.integrate as integrate
from scipy.interpolate import interp1d


Marvin = {
  #contains dictionaries about the rover
    "rover" : {
        "wheel_assembly" : { #contains definition about the rovers wheels inculuding details of what drives them
          "wheel" : {"radius" : 0.3 , "mass" : 1.0}, #radius - m, mass - kg
          "speed_reducer" : {"type" : "reverted", "diam_pinion" : 0.04, "diam_gear" : 0.07, "mass" : 1.5}, 
          "motor": {"torque_stall" : 170, "torque_noload" : 0, "speed_noload" : 3.80, "mass" : 5.0, "effcy_tau" : np.array([0, 10, 20, 40, 70, 165]), "effcy" : np.array([0, 0.60, 0.78, 0.73, 0.53, 0.04])},
        },
        "chassis": {"mass" : 659},   #define the mass of the chassis of our rover
        "science_payload" : {"mass" : 75},   #define the mass of the chassis
        "power_subsys" : {"mass" : 90},   #define the mass of the chassis
        "telemetry" : {"time" : np.empty(1), "completition_time" : 0, "velocity" : np.empty(1), "position": np.empty(1), "distance_traveled": 0, "max_velocity": 0, "average_velocity": 0, "power": np.empty(1), "battery_energy": 0, "energy_per_distance": 0}, #Telemetry
    },
    "planet" : {"g" : 3.72},
    
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

#input validation
  if not isinstance(omega, (np.ndarray, numbers.Number)):
    raise Exception("input speed should be a scalar or array")
  if isinstance(omega, np.ndarray) and not omega.ndim == 1:
    raise Exception("The rotaional velocity vector must only have one row")
  if not isinstance(motor, dict):
    raise Exception("Arg 2 should be dict")
  
#calculates the value of the tau
  tau = 0
  if isinstance(omega, np.ndarray):
    iter = omega.size
    tau = np.zeros(omega.size)
    for i in range(iter):
      if omega[i] > motor["speed_noload"]: # for case where omega > omega_nl
        tau[i] = 0
      elif omega[i] < 0: # for case where omega < 0
        tau[i] = motor["torque_stall"] 
      else: # for case where 0 <= omega < omega_nl
        tau[i] = motor['torque_stall'] - ((motor['torque_stall']-motor['torque_noload'])/motor['speed_noload'])*omega[i]
  else:
      for i in range(1):
        if omega > motor["speed_noload"]: # for case where omega > omega_nl
          tau = 0
        elif omega < 0: # for case where omega < 0
          tau = motor["torque_stall"] 
        else: # for case where 0 <= omega < omega_nl
          tau = motor['torque_stall'] - ((motor['torque_stall']-motor['torque_noload'])/motor['speed_noload'])*omega
  return tau

def get_gear_ratio(speed_reducer: dict):
  """
  Docstring for get_gear_ratio
  
  :param speed_reducer: Speed Reducer Data
  :type omega: dict
  """

  '''Returns the gear ratio of the speed reducer'''

  #input validation
  if not isinstance(speed_reducer, dict):
        raise Exception("Expected speed_reducer to be a dictionary.")
  if "type" not in speed_reducer:
        raise Exception("speed_reducer must contain a 'type' field.")
  if speed_reducer["type"].lower() != "reverted":
        raise Exception("Error: expected speed reducer type 'reverted'.")
  
  #Calculates and returns the gear ratio
  Ng = (speed_reducer["diam_gear"] / speed_reducer["diam_pinion"]) ** 2
  return Ng

def get_mass(rover: dict):
  """
  Docstring for get_mass
  
  :param rover: All rover data
  :type rover: dict
  """

  '''Returns the total mass of the rover in (kg)'''
  
  #input validation

  if not isinstance(rover, dict):
        raise Exception("Expected rover to be a dictionary.")
  
  #Mass of the rover is the sum of the mass of the chassis, science payload, power subsystem, and 6 times the mass of the wheel assembly (motor + speed reducer + wheel)

  m_chassis = rover["chassis"]["mass"]
  m_science = rover["science_payload"]["mass"]
  m_power = rover["power_subsys"]["mass"]
  m_motor = rover["wheel_assembly"]["motor"]["mass"]
  m_speed_reducer = rover["wheel_assembly"]["speed_reducer"]["mass"]
  m_wheel = rover["wheel_assembly"]["wheel"]["mass"]
  m =  m_chassis + m_science + m_power + 6 * (m_motor + m_speed_reducer + m_wheel)
  return m

def F_drive(omega: np.ndarray, rover: dict):
  """
  Docstring for F_drive
  
  :param omega: An array of shaft speeds
  :type omega: np.ndarray
  :param rover: All rover data
  :type rover: dict
  """

  '''Returns the resulting drive force of the rover in (N) given shaft speed, omega, in (rad/s)'''

  #input validation

  if not isinstance(omega, (np.ndarray, numbers.Number)):
    raise Exception("input speed should be a scalar or array")
  if not isinstance(rover, dict):
    raise Exception("Rover should be a dict")
  
  #Calculates the drive force using the formula Fd = 6 * Ng * tau / r, where Ng is the gear ratio, tau is the motor shaft torque, and r is the radius of the wheel
  Ng = get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])
  tau = tau_dcmotor(omega, rover["wheel_assembly"]["motor"])
  Fd = 6 * Ng * tau / rover["wheel_assembly"]["wheel"]["radius"] #6 wheels * gear_ratio * shaft torque / radius of the wheel
  return Fd

def F_gravity(terrain_angle: np.ndarray, rover: dict, planet: dict):
  """
  Docstring for F_gravity
  
  :param terrain_angle: An array of terrain angles in degrees
  :type terrain_angle: np.ndarray
  :param rover: All rover data
  :type rover: dict
  :param planet: All planet data
  :type planet: dict
  """

  '''Calculates the force of gravity on the rover in (N) given the terrain angle in degrees, the rover data, and the planet data'''

  #input validation
  if not isinstance(terrain_angle, (np.ndarray, numbers.Number)) and not isinstance(rover, dict) or not isinstance(planet, dict):
    raise Exception("Inputs are not the right data type.")
  if isinstance(terrain_angle, np.ndarray):
     print("true")
     if min(terrain_angle) < -75 or max(terrain_angle) > 75:
      raise Exception("To steep")
  elif terrain_angle < -75 or terrain_angle > 75:
     raise Exception("To steep")
  
  #calculates the x force of gravity
  if isinstance(terrain_angle, np.ndarray):
     Fgt = np.zeros(terrain_angle.size)
     m = get_mass(rover)
     for i in range(len(terrain_angle)): #Various terrain angles
        Fgt[i] = -1 * m * planet["g"] * np.sin(np.radians(terrain_angle[i]))
     return Fgt
  
  Fgt = 0
  m = get_mass(rover)
  Fgt = -1 * m * planet["g"] * np.sin(np.radians(terrain_angle))
  return Fgt

def F_rolling(omega: np.ndarray, terrain_angle: np.ndarray, rover: dict, planet: dict, Crr):
  """
  Docstring for F_rolling
  
  :param omega: An array of shaft speeds
  :type omega: np.ndarray
  :param terrain_angle: An array of terrain angles in degrees
  :type terrain_angle: np.ndarray
  :param rover: All rover data
  :type rover: dict
  :param planet: All planet data
  :type planet: dict
  :param Crr: Coefficient of rolling resistance
  :type Crr: Positive Scalar
  """

  '''Calculates the force of rolling resistance on the rover in (N) given the terrain angle in degrees, the rover data, the planet data, and the coefficient of rolling resistance'''

  #input validation

  if not isinstance(omega, (np.ndarray, numbers.Number)) or not isinstance(terrain_angle, (np.ndarray, numbers.Number)):
     raise Exception("Args 1/2 should be np.ndarray.")
  if not isinstance(rover, dict) or not isinstance(planet, dict):
      raise Exception("Args 3/4 should be dicts.")
  if Crr < 0:
    raise Exception("Crr must be a postive scalar")
  if isinstance(terrain_angle, np.ndarray):
     if min(terrain_angle) < -75 or max(terrain_angle) > 75:
      raise Exception("To steep")
     if omega.size != terrain_angle.size:
      raise Exception("omega and terrain_angle arrays must be the same size")
  else:
    if terrain_angle < -75 or terrain_angle > 75:
      raise Exception("To steep")
  
  #calculates the rolling force
  
  if isinstance(omega, np.ndarray):
    m = get_mass(rover)
    Ng = get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])
    Frr = np.zeros(omega.size)
    for i in range(omega.size): #Various terrain angles and speeds
      Fn = m * planet["g"] * np.cos(np.radians(terrain_angle[i]))
      Frr_simple = -Crr * Fn
      Frr[i] =  erf(40 * (omega[i] / Ng) * rover["wheel_assembly"]["wheel"]["radius"]) * Frr_simple
    return Frr
  
  m = get_mass(rover)
  Ng = get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])
  Fn = m * planet["g"] * np.cos(np.radians(terrain_angle))
  Frr_simple = -Crr * Fn
  Frr =  erf(40 * (omega / Ng) * rover["wheel_assembly"]["wheel"]["radius"]) * Frr_simple
  return Frr


def F_net(omega: np.ndarray, terrain_angle: np.ndarray, rover: dict, planet: dict, Crr: float):
  """
  Docstring for F_net
  
  :param omega: An array of shaft speeds
  :type omega: np.ndarray
  :param terrain_angle: An array of terrain angles in degrees
  :type terrain_angle: np.ndarray
  :param rover: All rover data
  :type rover: dict
  :param planet: All planet data
  :type planet: dict
  :param Crr: Coefficient of rolling resistance
  :type Crr: Positive Scalar
  """

  '''Calculates the net force on the rover in (N) given the terrain angle in degrees, the rover data, the planet data, and the coefficient of rolling resistance'''

  #input validation

  if not isinstance(omega, (np.ndarray, numbers.Number)) or not isinstance(terrain_angle, (np.ndarray, numbers.Number)):
     raise Exception("Args 1/2 should be np.ndarray.")
  if not isinstance(rover, dict) or not isinstance(planet, dict):
      raise Exception("Args 3/4 should be dicts.")
  if Crr <= 0:
    raise Exception("Your Crr input must be a postive input")
  if isinstance(omega,np.ndarray) and isinstance(terrain_angle, np.ndarray) and omega.size != terrain_angle.size:
     raise Exception("omega and terrain_angle must be equivalent length")
  minu = np.min(terrain_angle)
  maxu = np.max(terrain_angle)
  if minu < -75 or maxu > 75:
     raise Exception("To steep")
  
  #Calculates the net force using the formula Fnet = Fd + Fgt + Frr, where Fd is the drive force, Fgt is the x force of gravity, and Frr is the rolling resistance force
  Fd = F_drive(omega, rover)
  Fgt = F_gravity(terrain_angle, rover, planet)
  Frr = F_rolling(omega, terrain_angle, rover, planet, Crr)
  Fnet = Fd + Fgt + Frr
  return Fnet

def motorW(v: np.ndarray, rover: dict):
  """
  Docstring for motorW
  
  :param v: A 1 array of the rover's translational velocity in (m/s)
  :type v: np.ndarray
  :param rover: All rover data
  :type rover: dict
  """

  '''Returns the rotational speed of the motor shaft in (rad/s) given the translational velocity of the rover in (m/s) and the rover data'''

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
  """
  Docstring for rover_dynamics
  
  :param t: The time sample in seconds
  :type t: Scalar
  :param y: The state vector, a 2 array of the rover's translational velocity and position in (m/s) and (m)
  :type y: np.ndarray
  :param rover: All rover data
  :type rover: dict
  :param planet: All planet data
  :type planet: dict
  :param experiment: All experiment data
  :type experiment: dict
  """

  '''Returns the time derivative of the rover's translational velocity and position in (m/s^2) and (m/s) given the time, the rover's translational velocity and position, the rover data, the planet data, and the experiment data'''
  #input validation
  if not isinstance(t, numbers.Number):
    raise Exception("Time must be a scalar")
  if not isinstance(y, np.ndarray):
    raise Exception("The state vector must be a numpy array")
  if not isinstance(rover, dict):
    raise Exception("Rover should be a dict")
  if not isinstance(planet, dict):
    raise Exception("Planet should be a dict") 
  if not isinstance(experiment, dict):
    raise Exception("Experiment should be a dict")

  #original data interpolated between useing an cubic spline
  alpha_fun = interp1d(experiment['alpha_dist'], experiment['alpha_deg'], kind = 'cubic', fill_value='extrapolate') #fit the cubic spline
  terrain_angle = alpha_fun(y[1]).item() #terrain angle at state vector
  

  #caluates the acceleration and velocity at the state vector
  acel = (1/get_mass(rover))*F_net(motorW(y[0], rover), terrain_angle, rover, planet, experiment["Crr"])
  vcel = y[0]
  
  dydt = np.array([acel, vcel])

  return dydt



def mechpower(v: np.ndarray, rover: dict):
  """
  Docstring for mechpower
  
  :param v: A 1 array of the rover's translational velocity in (m/s)
  :type v: np.ndarray
  :param rover: All rover data
  :type rover: dict
  """

  '''Returns the mechanical power output of the motor in (W) given the translational velocity of the rover in (m/s) and the rover data'''

#input validation
  if not isinstance(v, (np.ndarray, numbers.Number)):
    raise Exception("The rotaional velocity of the rover must be in the form of a scalar or a vector")
  if isinstance(v, np.ndarray) and not v.ndim == 1:
    raise Exception("The rotaional velocity vector must only have one row")
  if not isinstance(rover, dict):
    raise Exception("The rover input must be a dictonary")
     
  P = tau_dcmotor(motorW(v,rover), rover["wheel_assembly"]["motor"]) * motorW(v,rover) #computes the mechaincal energy for one wheel
  
  return P

def battenergy(t: np.ndarray, v: np.ndarray, rover: dict):
  """
  Docstring for battenergy
  
  :param t: An array of time samples in seconds
  :type t: np.ndarray
  :param v: An array of the rover's translational velocity in (m/s)
  :type v: np.ndarray
  :param rover: All rover data
  :type rover: dict
  """

  '''Returns the rover energy consumed by the battery in (J) given an array of time samples, an array of the rover's translational velocity, and the rover data'''

  #input validation
  if np.size(t) != np.size(v):
    raise Exception("Time and velocity arrays must be the same length")
  if not isinstance(rover, dict):
    raise Exception("Rover should be a dict")
  
  #Define variables
  effcy_tau = rover["wheel_assembly"]["motor"]["effcy_tau"]
  effcy = rover["wheel_assembly"]["motor"]["effcy"]
  Nu = interp1d(effcy_tau, effcy, kind = 'cubic', fill_value='extrapolate') #fit the cubic spline

  #Calulculations
  P_batt = np.empty(len(t))
  for i in range(len(t)):
    P = mechpower(float(v[i]), rover)
    omega = motorW(float(v[i]), rover) #Calculates the rotational speed of the motor at the velocity v[i]
    tau = tau_dcmotor(omega,rover["wheel_assembly"]["motor"]) #calulates the value of our tau values
    eff_actual = Nu(tau)
    P_batt[i] = P / eff_actual #calculates the battery power at each time step
  E = integrate.trapezoid(P_batt, t) #integrate the power over time to get energy
  return 6 * E

def simulate_rover(rover: dict, planet: dict, experiment: dict, end_event: dict):
  """
  Docstring for simulate_rover
  
  :param rover: All rover data
  :type rover: dict
  :param planet: All planet data
  :type planet: dict
  :param experiment: All experiment data
  :type experiment: dict
  :param end_event: All end event Conditions
  :type end_event: dict
  """

  '''Returns all rover data from the experiment'''
  telemetry = rover["telemetry"]

  #input validation
  if not isinstance(rover, dict):
    raise Exception("Rover should be a dict")
  if not isinstance(planet, dict):
    raise Exception("Planet should be a dict")
  if not isinstance(experiment, dict):
    raise Exception("Experiment should be a dict")
  if not isinstance(end_event, list):
    raise Exception("End event should be a list")
  sol = integrate.solve_ivp(lambda t,y: rover_dynamics(float(t), y, rover, planet, experiment), experiment["time_range"], experiment["initial_conditions"], method="RK45", events = end_event)

  #Telemetry Values

  telemetry["time"] = sol.t
  telemetry["completition_time"] = telemetry["time"][-1]
  telemetry["velocity"] = sol.y[0,:]
  telemetry["position"] = sol.y[1,:]
  telemetry["distance_traveled"] = telemetry["position"][-1]
  telemetry["max_velocity"] = np.max(telemetry["velocity"])
  telemetry["average_velocity"] = telemetry["distance_traveled"] / telemetry["time"][-1]
  telemetry["power"] = 6 * mechpower(telemetry["velocity"], rover)
  telemetry["battery_energy"] = battenergy(telemetry["time"],telemetry["velocity"], rover)
  telemetry["batt_energy_per_distance"] = telemetry["battery_energy"] / telemetry["distance_traveled"]
  
  rover["telemetry"] = telemetry
  return rover