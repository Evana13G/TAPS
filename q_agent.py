import numpy as np
import random
from plane_state import PlaneState
import xpc
from time import sleep

GAMMA = 0.99
LAMBDA = 0.7
ALPHA = 0.01
EPSILON = 0.05

class QAgent:
  def __init__(self, state_vector_size, action_vector_size, weights = None):
    self.learning_mode = "Q"
    self.vector_size = state_vector_size + action_vector_size
    self.vector_size = 27
    weights = []
    for i in range(self.vector_size):
      weights.append(0.00)
    if (weights is not None):
      print "Weight passed in"
      self.weights = weights
    self.begin_learning()
    self.bias = 0.0
    self.eligibility_bias = 0.0

  def begin_learning(self):
    print "Begin learning"
    self.eligibility = []
    for i in range(self.vector_size):
      self.eligibility.append(0.00)

  def get_extra(self, state, action):
    return [state[8] * action[0], state[7] * action[1]]

  def evaluate(self, state, action):
    extra = self.get_extra(state, action)
    return sum([duo[0] * duo[1] for duo in zip(self.weights, state + action + extra)]) + self.bias

  def get_action(self, state, actions):
    if random.random() < EPSILON:
      action = random.sample(actions, 1)[0]
      self.last_action = (self.evaluate(state, action), state, action)
      return action

    (q, action) = max([(self.evaluate(state,action), action) for action in actions])
    self.last_action = (q, state, action)
    return action

  def update(self, reward):
    if (reward > 0.01):
      print "POSITIVE!"
    self.decay_traces(GAMMA * LAMBDA)
    self.add_traces(self.last_action[1], self.last_action[2])
    delta = reward - self.last_action[0]
    print "reward %f, expected %f, delta %f" % (reward, self.last_action[0], delta)
    self.update_weights((delta + GAMMA * self.last_action[0]) * ALPHA)
    print self.weights


  def update_weights(self, update):
    self.weights = [duo[0] + duo[1] * update for duo in zip(self.weights, self.eligibility)]
    self.bias += self.eligibility_bias * update
    return

  def decay_traces(self, update):
    self.eligibility = [e * update for e in self.eligibility]

  def add_traces(self, state, action):
    extra = self.get_extra(state, action)
    self.eligibility = [duo[0] + duo[1] for duo in zip(self.eligibility, state + action + extra)]


