import numpy as np
import random
from plane_state import PlaneState
import xpc
from time import sleep

GAMMA = 0.001
LAMBDA = 0.004

class QAgent:
  def __init__(self, state_vector_size, action_vector_size, weights = None):
    self.learning_mode = "Q"
    self.vector_size = state_vector_size + action_vector_size
    self.weights = [0.00] * (self.vector_size)
    if (weights is not None):
      self.weights = weights
    self.begin_learning()
    self.bias = 0
    self.eligibility_bias = 0

  def begin_learning(self):
    print "Begin learning"
    self.eligibility = [0.00] * (self.vector_size)

  def evaluate(self, state, action):
    return sum([duo[0] * duo[1] for duo in zip(self.weights, self.state + self.action)]) + self.bias

  def get_action(self, state, actions):
    (q, action) = max([(self.evaluate(state,action), action) for action in actions])
    self.last_action = (q, state, action)
    return action

  def update(self, reward):
    self.decay_traces(GAMMA * LAMBDA)
    self.add_traces(self.last_action[1], self.last_action[2])
    delta = reward - self.last_action[0]
    self.update_weights(delta + GAMMA * self.last_action[0])


  def update_weights(self, update):
    self.weights = [duo[0] + duo[1] * update for duo in zip(self.weights, self.eligibility)]
    self.bias += self.eligibility_bias * update
    return

  def decay_traces(self, update):
    self.eligibility = [e * update for e in self.eligibility]

  def add_traces(self, state, action):
    self.eligibility = [duo[0] + duo[1] for zip(self.eligibility, state + action)]