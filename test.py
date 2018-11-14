import planeState
from time import sleep


state = planeState.PlaneState(5691.52001953125, -7.349344253540039, -51844.9609375, 10)
print state.get_state_vector()

while True:
  print state.get_state_vector()
  sleep(1)