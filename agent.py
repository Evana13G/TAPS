import numpy as np
import random
from plane_state import PlaneState
import xpc
from time import sleep

class Agent:
  def __init__(self, _learning_mode, _w, discount_factor):
    self.learning_mode = _learning_mode
    self.W = _w
    self.gamma = discount_factor

  def beginLearning(self):
    print "Begin learning"

  def get_action(self, state, actions):
    return random.choice(actions)

  def update(self, state, action, reward):
    pass

  def get_qval(seld, state, action):
    q = 0
    numStateFeatures = len(state)

    for i in range(numStateFeatures):
      q = q + (state[i] * self.W[i])
    for i in range(len(action)):
      q = q + (state[i] * self.W[i + numStateFeatures])

    return q