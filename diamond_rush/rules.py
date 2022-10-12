#!/usr/bin/env python3
from agent import Agent

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
# 'A' agent over spike
# '@' agent over key with key
# agent over button
# rock over button

def check_past(i, j, p_state, state):

  if p_state == state:
    return state

  if p_state[i,j] == 's':
    state[i,j] == 'w'

  elif state[i,j] == 'R': # rock over spike
    pass

  return state

def check_rules(agent: Agent, p_state, state):
  i, j = agent.get_pos()
  ni, nj = agent.play(state)
#  p_state = state

### is previous state necesary? maybe for spikes but not saving the whole matrix
  # save state when move again spikes up!
  if state[ni,nj] == 's': # spikes
    state[ni,nj] = 'a'

  elif state[ni,nj] =='p':  # path
    state[ni,nj] = 'a'
    state[i,j] = 'p'
    agent.move([ni,nj])

  elif state[ni,nj] == 'g': # goal
    # TODO: change state iff all diamonds are collected!!!
    state[ni,nj] = 'a'
    state[i,j] = 'p'
    agent.move([ni,nj])

  elif state[ni,nj] =='K': # kdoors
    if agent.has_key():
      state[ni,nj] = 'a'
    
  elif state[ni,nj] == 'k': # keys
    if agent.has_key():
      state[ni,nj] = '@' # '@' agent over key with key
    else:
      state[ni,nj] = 'a'

  elif state[ni,nj] == 'd': # diamonds
### Should count collected diamonds?
    state[ni,nj] = 'a'
    state[i,j] = 'p'
    agent.move([ni,nj])

  elif state[ni,nj] == 'b': # button
    pass

  elif state[ni,nj] == 'h': # holes
    pass

  elif state[ni,nj] == 'B': # bDoor
    pass

  elif state[ni,nj] == 'r': # rock
    pass
  else:
    print('################## not smart #######################')

  return p_state, state
