#!/usr/bin/env python3

# 'p' path
# 's'  spikes

# 'a'  agent
# 'A' agent over spike
# '@' agent over key with key
# '_'  agent over button
# 'g'  goal

# 'K'  kdoor
# 'k'  key
# 'l'  lava
# 'w'  wall
# 'd'  diamond
# 'h'  hole

# 'B'  bDoor
# 'b'  button

# 'r'  rock
# 'R' rock over spike
# 'o' rock over button
# 'D' rock over diamond

# Level 12 & 7 are the most complex

### TODO: check past for spikes up
def check_past(i, j, p_state, state):

  if p_state == state:
    return state

  if p_state[i,j] == 's':
    state[i,j] == 'w'

  elif state[i,j] == 'R': # rock over spike
    pass

  return state

# 'a' agent
# 'A' agent over spike
# '@' agent over key with key
# '_' agent over button

def agent():
  pass

def agent_over_button():
  pass

def agent_over_spike():
  pass

def agent_over_kk():
  pass

def check_rules(agent: Agent, p_state, state):
  i, j = agent.get_pos()
  ni, nj = agent.play(state)

  if state[i, j] == 'a':
    agent(state, (i, j), (ni, nj))
  elif state[i, j] == 'A':
    agent_over_spike(state, (i, j), (ni, nj))
  elif state[i, j] == '@':
    agent(state, (i, j), (ni, nj))
  elif state[i, j] == '_':
    agent_over_button(state, (i, j), (ni, nj))
  else:
    agent_over_kk(state, (i, j), (ni, nj))


### is previous state necesary? maybe for spikes but not saving the whole matrix
  # save state when move again spikes up!
  if state[ni,nj] == 's': # spikes
    state[ni,nj] = 'A'
    state[i, j] = 'p'

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
  # check rock direction
    pass
  else:
    print('################## not smart #######################')

  return p_state, state
