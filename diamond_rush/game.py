#!/usr/bin/env python3

#from rules import rules
import numpy as np
from agent import Agent

# Levels with buttons: 8, 9, 11, 12, 13, 14, 15, 17, 18, 19
class Game:
  def __init__(self, level, a_pos):
    self.level = self.parseLevel(level) 
    self.a_pos = a_pos
    self.state, self.f_state = self.load_level(self.level, self.a_pos)
    self.diamonds = self.diamonds_pos(self.state)
    self.g_pos = self.goal_pos(self.state)
    self.finish = False

  def load_level(self, level, a_pos): 
    state = np.loadtxt('./levels/default_init_states/' + level, dtype=str)
    f_state = np.loadtxt('./levels/final_states/' + level, dtype=str)

    if a_pos != self.agent_pos(state):
      # TODO: update new state with agent new position
      new_state = state
      return new_state, f_state

    return state, f_state

  def parseLevel(self, level):
    level = level.split('/')
    level = level[2][:len(level[2])-4]
    return level

  def goal_pos(self, state):
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'g':
          return (i, j)

  def diamonds_pos(self, state):
    pos = []
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'd' or state[i,j] == 'D':
          pos.append((i,j))
    return pos 

  def agent_pos(self, state):
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'a' or state[i,j] == 'A' or state[i,j] == '@':
          return i,j

"""
state = np.loadtxt('./levels/default_init_states/11', dtype=str)
for i in range(len(state)):
  for j in range(len(state[0])):
    if state[i,j] == 'b':
      print('button:', i, j)

for i in range(len(state)):
  for j in range(len(state[0])):
    if state[i,j] == 'B':
      print('door:', i, j)
"""
