#!/usr/bin/env python3
import cv2 
import numpy as np
import os
from rules import check_rules

#is_0 = np.loadtxt('./levels/default_init_states/0',dtype=str)
#fs_0 = np.loadtxt('./levels/final_states/0',dtype=str)
#print('init state 0:') 
#print(is_0)

### set up level... its variables,and state 
class Level:
  diamonds = 0
  def __init__(self, level, a_pos):
    self.level = level
    self.a_pos = a_pos
    self.state, self.f_state = self.load_level(self.level, self.a_pos)
    self.p_state = self.state

  def get_state(self):
    return self.state
# TODO: define structure for previous and new state
  def new_state(self, a_move):
    self.p_state, self.state = check_rules(self.a_pos, a_move, self.p_state, self.state)
    return self.state

  def load_level(self, level, a_pos): 
    # TODO: concatenate level with txt file
    state = np.loadtxt('./levels/default_init_states/0',dtype=str)
    f_state = np.loadtxt('./levels/final_states/0',dtype=str)
    if a_pos != self.agent_pos(state):
      # TODO: update new state with agent new position
      new_state = state
      return new_state, f_state
    return state, f_state

  def agent_pos(self, state):
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'a':
          return i,j

### manage interactions btw Level and Agent... and it captures image of enviroment, dk if rules goes here or in level
class Enviroment:
  ### TODO: check if agent has change pos, add metadata of levels as txt... add rules
  ### TODO probably need to remember 2 states back for spikes and some rocks interactions...
  def __init__(self):
    pass

i = [5,2]
level = Level(1,i)
print(level.get_state())
print('pos ', level.agent_pos(level.get_state()))
print()
l = [0,-1]
#print(l[1])
print(level.new_state(l))
print('new pos ', level.agent_pos(level.get_state()))
