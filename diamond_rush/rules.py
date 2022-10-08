#!/usr/bin/env python3
import numpy as np

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
