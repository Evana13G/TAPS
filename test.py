from plane_state import PlaneState
from flight_manager import FlightManager
from time import sleep


# state = planeState.PlaneState(5691.52001953125, -7.349344253540039, -51844.9609375, 10)
# print state.get_state_vector()

# while True:
#   print state.get_state_vector()
#   sleep(1)

flightManager = FlightManager()


aircraftData = {}
aircraftData['lat'] = 37.524
aircraftData['lon'] = -122.06899
aircraftData['alt'] = 2500
aircraftData['pitch'] = 0
aircraftData['roll'] = 0
aircraftData['heading'] = 0
aircraftData['gear'] = 1
aircraftData['attack'] = [18,   0, -998,   0, -998, -998, -998, -998, -998]
aircraftData['velocity'] = [ 3, 130,  130, 130,  130, -998, -998, -998, -998]
aircraftData['orientation'] = [16,   0,    0,   0, -998, -998, -998, -998, -998]


flightManager.startFlight(aircraftData)
print "Started Flight"


aircraftData['pitch'] = 1
aircraftData['roll'] = 0
aircraftData['heading'] = 0
flightManager.maneuverAircraft(aircraftData)
print "Finished Maneuver 1 (pitch)"
sleep(2)

aircraftData['pitch'] = -1
aircraftData['roll'] = 0
aircraftData['heading'] = 0
flightManager.maneuverAircraft(aircraftData)
print "Finished Maneuver 2 (pitch)"
sleep(2)


aircraftData['pitch'] = 0
aircraftData['roll'] = 1
aircraftData['heading'] = 0
flightManager.maneuverAircraft(aircraftData)
print "Finished Maneuver 3 (roll)"
sleep(2)


aircraftData['pitch'] = 0
aircraftData['roll'] = -1
aircraftData['heading'] = 0
flightManager.maneuverAircraft(aircraftData)
print "Finished Maneuver 4 (roll)"
sleep(2)


aircraftData['pitch'] = 0
aircraftData['roll'] = 0
aircraftData['heading'] = 1
flightManager.maneuverAircraft(aircraftData)
print "Finished Maneuver 5 (heading)"
sleep(2)

aircraftData['pitch'] = 0
aircraftData['roll'] = 0
aircraftData['heading'] = -1
flightManager.maneuverAircraft(aircraftData)
print "Finished Maneuver 6 (heading)"
sleep(2)
