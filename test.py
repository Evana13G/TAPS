from plane_state import PlaneState
from flight_manager import FlightManager
from time import sleep
from agent import Agent
from q_agent import QAgent
import sys

# state = planeState.PlaneState(5691.52001953125, -7.349344253540039, -51844.9609375, 10)
# print state.get_state_vector()

# while True:
#   print state.get_state_vector()
#   sleep(1)
args = sys.argv
args.pop(0)
weight = [float(arg) for arg in args]
if not weight:
  agent = QAgent(54, 7, 12)
else:
  agent = QAgent(54, 7, weight)

flightManager = FlightManager(agent, "apha 0.0005")

print "Starting Flight"
while True:
  flightManager.run_episode()
