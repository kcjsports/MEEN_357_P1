"""###########################################################################
#   Defines mission events.
#
#   Created by: Former Marvin Numerical Methods Engineering Team
#   Last Modified: 22 October 2021
###########################################################################"""

def define_mission_events():
        
    mission_events = {'alt_heatshield_eject' : 8000, # Altitude to eject heatshield
                      'alt_parachute_eject' : 900, # Altitude to eject parachute
                      'alt_rockets_on' : 1800, # Altitude to activate rockets
                      'alt_skycrane_on' : 7.6} # Altitude to activate skycrane
    return mission_events