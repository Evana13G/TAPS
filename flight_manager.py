import numpy as np
import random
from plane_state import PlaneState
import xpc
from time import sleep

class FlightManager:
  def __init__(self):
    self.duration = 90
    self.client = None
    self.state = PlaneState()

  def startFlight(self, aircraftData):
    print "Setting up simulation"
    self.client = xpc.XPlaneConnect()

    # Verify connection
    try:
        # If X-Plane does not respond to the request, a timeout error
        # will be raised.
        self.client.getDREF("sim/test/test_float")
    except:
        print "Error establishing connection to X-Plane."
        print "Exiting..."
        return

    # Set position of the player aircraft
    print "Setting position"
    #       Lat     Lon         Alt   Pitch Roll Yaw Gear
    # posi = [37.524, -122.06899, 2500, 0,    0,   0,  1]
    posi = [aircraftData['lat'],
    		aircraftData['lon'],
    		aircraftData['alt'],
        	aircraftData['pitch'],
        	aircraftData['roll'],
        	aircraftData['heading'],
        	aircraftData['gear']]
    self.client.sendPOSI(posi)

    # Set position of a non-player aircraft
    # print "Setting NPC position"
    #       Lat       Lon         Alt   Pitch Roll Yaw Gear
    # posi = [37.52465, -122.06899, 2500, 0,    20,   0,  1]
    # client.sendPOSI(posi, 1)

    # Set angle of attack, velocity, and orientation using the DATA command
    print "Setting orientation"
    # data = [\
    #     [18,   0, -998,   0, -998, -998, -998, -998, -998],\
    #     [ 3, 130,  130, 130,  130, -998, -998, -998, -998],\
    #     [16,   0,    0,   0, -998, -998, -998, -998, -998]\
    #     ]
    # data = [\
    #     aircraftData['attack'],\
    #     aircraftData['velocity'],\
    #     aircraftData['orientation']\
    #     ]
    data = [aircraftData['attack'], aircraftData['velocity'], aircraftData['orientation']]
    self.client.sendDATA(data)

    # Set control surfaces and throttle of the player aircraft using sendCTRL
    print "Setting controls"
    ctrl = [0.0, 0.0, 0.0, 0.8]
    self.client.sendCTRL(ctrl)

    # Pause the sim
    # print "Pausing"
    # client.pauseSim(True)
    # sleep(2)

    # Toggle pause state to resume
    # print "Resuming"
    # client.pauseSim(False)

    # Stow landing gear using a dataref
    # print "Stowing gear"
    # gear_dref = "sim/cockpit/switches/gear_handle_status"
    # client.sendDREF(gear_dref, 0)

    # Let the sim run for a bit.
    # sleep(4)

    # Make sure gear was stowed successfully
    # gear_status = self.client.getDREF(gear_dref)
    # if gear_status[0] == 0:
    #     print "Gear stowed"
    # else:
    #     print "Error stowing gear"

    # raw_input("Press any key to exit...")
    while True:
        sleep(0.5)
        maneuverAircraft(None)


  def maneuverAircraft(self, params):
    self.client.sendCTRL(random.choice(state.get_action_vectors())




