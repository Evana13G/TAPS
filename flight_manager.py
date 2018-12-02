import numpy as np
import random
from plane_state import PlaneState
import reward_functions
import xpc
from time import sleep

# This essentially drives all production
class FlightManager:

  def __init__(self, pilot):
    self.duration = 90
    self.client = xpc.XPlaneConnect()
    self.state = PlaneState(0,0,0,0, reward_functions.fly_flat_reward)
    self.agent = pilot
    self.episode = 0
    self.startLocation = {
      'lat': 37.524,
      'lon': -122.06899,
      'alt': 2500,
      'pitch': 0,
      'roll': 0,
      'heading': 0,
      'gear': 1,
      'attack': [18, 0, -998,   0, -998, -998, -998, -998, -998],
      'velocity': [ 3, 130,  130, 130,  130, -998, -998, -998, -998],
      'orientation': [16,   0,    0,   0, -998, -998, -998, -998, -998],
    }
    self.total_reward = 0


  def run_episode(self):
    print "New episode"
    self.episode = self.episode + 1
    self.client.pauseSim(True)
    self.start_flight(self.startLocation)
    self.agent.begin_learning()
    self.client.pauseSim(False)
    step_count = 0
    episode_reward = 0
    while True and step_count < 1000:
      state_vector = self.state.get_normalized_state_vector()
      action_vectors = self.state.get_action_vectors()
      action = self.agent.get_action(state_vector, action_vectors)
      self.client.sendCTRL(action)
      sleep(0.2)
      reward = self.state.get_reward()
      episode_reward += reward
      self.total_reward += reward
      self.agent.update(reward)
      step_count += 1
      print "%d, %d, %d, %d" % (self.episode, step_count, reward, episode_reward)



  def start_flight(self, aircraftData):
    # Set position of the player aircraft
    print "Resetting position"
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

    print "Setting orientation"
    data = [aircraftData['attack'], aircraftData['velocity'], aircraftData['orientation']]
    self.client.sendDATA(data)



