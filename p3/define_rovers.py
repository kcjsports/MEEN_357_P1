"""###########################################################################
#   This file initializes a rover structure for testing/grading
#
#   Created by: Former Marvin Numerical Methods Engineering Team
#   Last Modified: 28 October 2023
###########################################################################"""

import numpy as np

def define_rover_1():
    # Initialize Rover dict for testing
    wheel = {'radius':0.30, # Radius of rover wheel
             'mass':1} # Mass of rover wheel
    speed_reducer = {'type':'reverted', # Gearbox type
                     'diam_pinion':0.04, # Diameter of pinion gear
                     'diam_gear':0.07, # Diameter of drive gear
                     'mass':1.5} # Mass of gearbox
    motor = {'torque_stall':170, # Stall torque of rover motor
             'torque_noload':0, # Free spin torque of rover motor
             'speed_noload':3.80, # Free spin max speed of rover motor
             'mass':5.0} # Mass of rover motor
    
    # phase 2 add ##############################
    motor['effcy_tau'] = np.array([0, 10, 20, 40, 70, 165])
    motor['effcy']     = np.array([0,.55,.75,.71,.5, .05])
    #############################################
        
    chassis = {'mass':659} # Mass of rover chassis
    science_payload = {'mass':75} # Mass of science payload
    power_subsys = {'mass':90} # Mass of power subsystem
    
    wheel_assembly = {'wheel':wheel, # See wheel
                      'speed_reducer':speed_reducer, # See speed_reducer
                      'motor':motor} # See motor
    
    rover = {'wheel_assembly':wheel_assembly, # See wheel_assembly
             'chassis':chassis, # See chassis
             'science_payload':science_payload, # See science_payload
             'power_subsys':power_subsys} # See power_subsys
    
    # planet = {'g':3.72}
    
    # return only the rover now
    return rover #, planet

def define_rover_2():
    # Initialize Rover dict for testing
    wheel = {'radius':0.30, # Radius of rover wheel
             'mass':2}  # Mass of rover wheel
    speed_reducer = {'type':'reverted', # Gearbox type
                     'diam_pinion':0.04, # Diameter of pinion gear
                     'diam_gear':0.06, # Diameter of drive gear
                     'mass':1.5} # Mass of gearbox
    motor = {'torque_stall':180, # Stall torque of rover motor
             'torque_noload':0, # Free spin torque of rover motor
             'speed_noload':3.70, # Free spin max speed of rover motor
             'mass':5.0} # Mass of rover motor
    
    
    # phase 2 add ##############################
    motor['effcy_tau'] = [0, 10, 20, 40, 75, 165]
    motor['effcy']     = [0,.60,.75,.73,.55, .05]
    #############################################
    
    
    chassis = {'mass':659} # Mass of rover chassis
    science_payload = {'mass':75} # Mass of science payload
    power_subsys = {'mass':90} # Mass of power subsystem
    
    wheel_assembly = {'wheel':wheel, # See wheel
                      'speed_reducer':speed_reducer, # See speed_reducer
                      'motor':motor} # See motor
    
    rover = {'wheel_assembly':wheel_assembly, # See wheel_assembly
             'chassis':chassis, # See chassis
             'science_payload':science_payload, # See science_payload
             'power_subsys':power_subsys} # See power_subsys
    
    # planet = {'g':3.72}
    
    # return only the rover now
    return rover #, planet

def define_rover_3():
    # Initialize Rover dict for testing
    wheel = {'radius':0.30, # Radius of rover wheel
             'mass':2}  # Mass of rover wheel
    speed_reducer = {'type':'standard', # Gearbox type
                     'diam_pinion':0.04, # Diameter of pinion gear
                     'diam_gear':0.06, # Diameter of drive gear
                     'mass':1.5} # Mass of gearbox
    motor = {'torque_stall':180, # Stall torque of rover motor
             'torque_noload':0, # Free spin torque of rover motor
             'speed_noload':3.70, # Free spin max speed of rover motor
             'mass':5.0} # Mass of rover motor
    
    
    # phase 2 add ##############################
    motor['effcy_tau'] = [0, 10, 20, 40, 75, 165]
    motor['effcy']     = [0,.60,.75,.73,.55, .05]
    #############################################
    
    
    chassis = {'mass':659} # Mass of rover chassis
    science_payload = {'mass':75} # Mass of science payload
    power_subsys = {'mass':90} # Mass of power subsystem
    
    wheel_assembly = {'wheel':wheel, # See wheel
                      'speed_reducer':speed_reducer, # See speed_reducer
                      'motor':motor} # See motor
    
    rover = {'wheel_assembly':wheel_assembly, # See wheel_assembly
             'chassis':chassis, # See chassis
             'science_payload':science_payload, # See science_payload
             'power_subsys':power_subsys} # See power_subsys
    
    # planet = {'g':3.72}
    
    # return only the rover now
    return rover #, planet


def define_rover_4():
    # Initialize Rover dict for testing
    wheel = {'radius':0.20, # Radius of rover wheel
             'mass':2}  # Mass of rover wheel
    speed_reducer = {'type':'reverted', # Gearbox type
                     'diam_pinion':0.04, # Diameter of pinion gear
                     'diam_gear':0.06, # Diameter of drive gear
                     'mass':1.5} # Mass of gearbox
    motor = {'torque_stall':165, # Stall torque of rover motor
             'torque_noload':0, # Free spin torque of rover motor
             'speed_noload':3.85, # Free spin max speed of rover motor
             'mass':5.0} # Mass of rover motor
    
    # phase 2 add ##############################
    motor['effcy_tau'] = np.array([0, 10, 20, 40, 75, 170])
    motor['effcy']     = np.array([0,.60,.75,.73,.55, .05])
    #############################################
    
    
    chassis = {'mass':674} # Mass of rover chassis
    science_payload = {'mass':80} # Mass of science payload
    power_subsys = {'mass':100} # Mass of power subsystem
    
    wheel_assembly = {'wheel':wheel, # See wheel
                      'speed_reducer':speed_reducer, # See speed_reducer
                      'motor':motor} # See motor
    
    rover = {'wheel_assembly':wheel_assembly, # See wheel_assembly
             'chassis':chassis, # See chassis
             'science_payload':science_payload, # See science_payload
             'power_subsys':power_subsys} # See power_subsys
    
    # planet = {'g':3.72}
    
    # return only the rover now
    return rover #, planet