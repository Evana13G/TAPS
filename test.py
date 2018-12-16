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
agent = None
if not weight:
  agent = QAgent(17, 6)
else:
  agent = QAgent(17, 6, weight)

# agent = Agent()

flightManager = FlightManager(agent)

print "Starting Flight"
episodes = 0
while episodes < 5:
  flightManager.run_episode()
  episodes = episodes + 1