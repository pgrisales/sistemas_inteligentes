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
# 'R' rock over spike

def check_past(i, j, p_state, state):

  if p_state == state:
    return state

  if p_state[i,j] == 's':
    state[i,j] == 'w'

  elif state[i,j] == 'R': # rock over spike
    pass

  return state

def check_rules(a_pos, a_move, p_state, state):
  i, j = a_pos[0], a_pos[1]
  ni, nj = i + a_move[0], j + a_move[1]
  # save state when move again spikes up!
  if state[ni,nj] == 's': # spikes
    state[ni,nj] == 'a'

  elif state[ni,nj] =='p':  # path
    print('ispath')
    p_state = state
    state[ni,nj] = 'a'
    state[i,j] = 'p'

  # how to represent agent with or without keys!
  elif state[ni,nj] =='K': # kdoors
    pass

  elif state[ni,nj] == 'g': # goal
    # iff all diamonds are collected!
    if all_diamonds:
      state[ni,nj] == 'a'
    
  elif state[ni,nj] == 'k': # keys
    pass
  elif state[ni,nj] == 'l': # lava
    pass
  elif state[ni,nj] == 'w': # wall
    pass
  elif state[ni,nj] == 'd': # diamonds
    pass
  elif state[ni,nj] == 'b': # button
    pass
  elif state[ni,nj] == 'h': # holes
    pass
  elif state[ni,nj] == 'B': # bDoor
    pass
  elif state[ni,nj] == 'r': # rock
    pass

  return p_state, state
