#!/usr/bin/env python3
import numpy as np

is_0 = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)
fs_0 = np.loadtxt('./levels/final_states/0',dtype=str)#.reshape(15,10)
print('init state 0:') 
print(is_0)
#print('final state 0:') 

def agentPos(state):
  for i in range(0,len(state)):
    for j in range(0,len(state[0])):
      if state[i,j] == 'a':
        return i,j

i,j = agentPos(is_0)
print(i,j)

# 'a'  agent
# 's'  spikes
# 'K'  kdoors
# 'g'  goal
# 'k'  keys
# 'l'  lava
# 'w'  wall
# 'd'  diamonds
# 'b'  button
# 'h'  holes
# 'B'  bDoor
# 'r'  rock

class Agent:
  def __init__(self,pos)
    pass

  def move(i,j):
    pass

def setGoals():
  pass

class Eviroment:
  def __init__(self,M)
    pass

def rules(state, aMove):
  # save state when move again spikes up!
  if state[i,j] = 's': # spikes
    state[i,j] == 'a'

  # how to represent agent with or without keys!
  elif state[i,j] = 'K': # kdoors
    pass

  elif state[i,j] = 'g': # goal
    # iff all diamonds are collected!
    if all_diamonds:
      state[i,j] == 'a'
    
  elif state[i,j] = 'k': # keys
    pass
  elif state[i,j] = 'l': # lava
    pass
  elif state[i,j] = 'w': # wall
    pass
  elif state[i,j] = 'd': # diamonds
    pass
  elif state[i,j] = 'b': # button
    pass
  elif state[i,j] = 'h': # holes
    pass
  elif state[i,j] = 'B': # bDoor
    pass
  elif state[i,j] = 'r': # rock
    pass

  return state
