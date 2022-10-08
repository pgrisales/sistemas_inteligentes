#!/usr/bin/env python3
import cv2 
import numpy as np
import os

is_0 = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)
fs_0 = np.loadtxt('./levels/final_states/0',dtype=str)#.reshape(15,10)
print('init state 0:') 
print(is_0)

def agentPos(state):
  for i in range(0,len(state)):
    for j in range(0,len(state[0])):
      if state[i,j] == 'a':
        return i,j

i,j = agentPos(is_0)
print(i,j)

### set up level... its variables,and state 
class Level:
  diamonds = 0
  state = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)
  def __init__(self,whichLevel):
    self.level = whichLevel

### manage interactions btw Level and Agent... and it captures image of enviroment, dk if rules goes here or in level
class Enviroment:
#  level = Level(whichLevel())
#  state = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)
  ### TODO: check if agent has change pos, add metadata of levels as txt... add rules
  ### TODO probably need to remember 2 states back for spikes and some rocks interactions...
  
  def __init__(self):
    pass

