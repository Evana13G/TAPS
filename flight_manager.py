import numpy as np
import random
from plane_state import PlaneState
import reward_functions
import xpc
from time import sleep
import csv

# This essentially drives all production
class FlightManager:

  def __init__(self, pilot, pilot_name):
    self.duration = 90
    self.client = xpc.XPlaneConnect()
    self.state = PlaneState(0,0,0,0, reward_functions.fly_flat_reward)
    self.agent = pilot
    self.name = pilot_name
    self.episode = 0
    self.steps_overall = 0
    self.startLocation = {
      'lat': 37.524,
      'lon': -122.06899,
      'alt': 2500,
      'pitch': 0,
      'roll': 0,
      'heading': 0,
      'gear': 0,
      'attack': [18, 0, -998,   0, -998, -998, -998, -998, -998],
      'velocity': [ 3, 300,  300, 300,  130, -998, -998, -998, -998],
      'orientation': [16,   0,    0,   0, -998, -998, -998, -998, -998],
    }
    self.total_reward = 0
    self.reward_curve_data = []

  def run_episode(self):
    print "New episode"
    self.episode = self.episode + 1
    self.client.pauseSim(True)
    self.start_flight(self.startLocation)
    self.agent.begin_learning()
    self.client.pauseSim(False)
    step_count = 0
    episode_reward = 0
    while True and step_count < 500:
      state_vector = self.state.get_normalized_state_vector()
      action_vectors = self.state.get_action_vectors()
      action = self.agent.get_action(state_vector, action_vectors)
      self.client.sendCTRL(action)
      sleep(0.1)
      reward = self.state.get_reward()
      episode_reward += reward
      self.total_reward += reward
      self.agent.update(reward)
      step_count += 1
      self.steps_overall += 1
      print "%d, %d, %d, %d" % (self.episode, step_count, reward, episode_reward)
      self.reward_curve_data.append([self.episode, step_count, reward, episode_reward, self.steps_overall, self.total_reward])
    self.reward_curve_data_to_CSV()



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

  def reward_curve_data_to_CSV(self):
     with open('reward_curve_data.csv', mode='a') as rcd_f:
       rcd_w = csv.writer(rcd_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       for dataPoint in self.reward_curve_data:
         rcd_w.writerow([self.name, dataPoint[0], dataPoint[1], dataPoint[2], dataPoint[3], dataPoint[4], dataPoint[5]])

