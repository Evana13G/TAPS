from plane_state import PlaneState
from flight_manager import FlightManager
from time import sleep
from agent import Agent

# state = planeState.PlaneState(5691.52001953125, -7.349344253540039, -51844.9609375, 10)
# print state.get_state_vector()

# while True:
#   print state.get_state_vector()
#   sleep(1)

agent = Agent()

flightManager = FlightManager(agent)

print "Starting Flight"
flightManager.run_episode()
