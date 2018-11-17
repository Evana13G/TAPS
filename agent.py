import numpy as np
import random
from plane_state import PlaneState
import xpc
from time import sleep

class Agent:
  def __init__(self):
    self.learning_mode = "Q"

  def beginLearning(self):
    print "Begin learning"

  def get_action(self, state, actions):
    return random.choice(actions)

  def update(self, state, action, reward):
    pass