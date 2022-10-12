#!/usr/bin/env python3
import cv2 
import numpy as np
import os
from rules import check_rules
from agent import Agent

#is_0 = np.loadtxt('./levels/default_init_states/0',dtype=str)
#fs_0 = np.loadtxt('./levels/final_states/0',dtype=str)
#print('init state 0:') 
#print(is_0)

class Level:
### TODO: should count variables like diamonds?
  diamonds = 0
  def __init__(self, level, a_pos):
    self.level = level
    # default init agent pos 
    self.a_pos = a_pos
    self.state, self.f_state = self.load_level(self.level, self.a_pos)
    self.p_state = self.state
    # remeber previous state
#    self.p_state = self.state

  def get_state(self):
    return self.state

  def get_f_state(self):
    return self.f_state

# TODO: define structure for previous and new state
  def new_state(self, agent: Agent):
    self.p_state, self.state = check_rules(agent, self.p_state, self.state)
    return self.state

  def load_level(self, level, a_pos): 
    #'./levels/1.png'
    level = level.split('/')
    level = level[2][:len(level[2])-4]

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
        if state[i,j] == 'a' or state[i,j] == 'A' or state[i,j] == '@':
          return i,j

### manage interactions btw Level and Agent... and it captures image of enviroment, dk if rules goes here or in level
class Enviroment:
  ### TODO: check if agent has change pos, add metadata of levels as txt... add rules
  ### TODO probably need to remember 2 states back for spikes and some rocks interactions...
  def __init__(self):
    pass
  def run(self):
    i = [5,2] # Default init pos level 0
    tempL = './levels/1.png'
    level = Level(tempL,i)
    agent = Agent(i)
#    for i in range(3):
#      print(level.get_state())
#      print(agent.get_pos())
#      print()
#      level.new_state(agent, agent.play())
    i = 1
    while not np.array_equal(level.get_state(), level.get_f_state()):
      print(level.new_state(agent))
      #print(level.get_state())
      
      print('##### ', agent.get_pos(), ' ####')
      print('##### ', i, ' ####')
      i += 1

env = Enviroment()
env.run()
"""
i = [5,2] # Default init pos level 0
level = Level(1,i)
agent = Agent(i)
a = agent.play()
print(a[0])
print(level.get_state())
print('pos ', level.agent_pos(level.get_state()))
print()
l = [0,-1]
#print(l[1])
print(level.new_state(l))
print('new pos ', level.agent_pos(level.get_state()))
"""
