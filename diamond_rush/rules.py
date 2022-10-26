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

# 'a' agent
# 'A' agent over spike
# '@' agent over key with key
# '_' agent over button

def rules(agent: Agent, state):
  i, j = agent.get_pos()
  ni, nj = agent.play(state)
  a_state = state[i, j]
  wall = ['h', 'w', 'l']

  if a_state == 'a':
    state[i, j] = 'p'
    
  elif a_state == 'A':
    state[i, j] = 'w'

  elif a_state == '_':
    state[i, j] = 'p'

  else:
    state[i, j] = 'k'

# Done
  if state[ni,nj] == 's':       # spike
    state[ni,nj] = 'A'

# Done
  elif state[ni,nj] == 'p':     # path
    state[ni,nj] = 'a'

# Done
  elif state[ni,nj] == 'k':     # key
    if agent.has_key():
      state[ni,nj] = '@' 
    else:
      state[ni,nj] = 'a'
      agent.set_has_key(True)

# Done
  elif state[ni,nj] in wall:     # hole, wall, lava
    state[i, j] = a_state

  elif state[ni,nj] == 'r':     # rock
    nri, nrj = ni + (ni-i), nj + (nj-j)
    w = ['w','r','K','B']

    if state[nri, nrj] in w:
      state[i, j] = a_state

    elif state[nri, nrj] == 'l'
      state[ni, nj] = 'a'

    # define button -> doors
    elif state[nri, nrj] == 'b'
      state[ni, nj] = 'a'
      state[nri, nrj] = 'o'

    elif state[nri, nrj] == 's'
      state[ni, nj] = 'a'
      state[nri, nrj] = 'R'
      
    elif state[nri, nrj] == 'd'
      state[ni, nj] = 'a'
      state[nri, nrj] = 'R'

  elif state[ni,nj] == 'R':     # rock over spike 
    if agent.has_key():

  elif state[ni,nj] == 'o':     # rock over button
    if agent.has_key():

  elif state[ni,nj] == 'D':     # rock over diamond
    if agent.has_key():

  elif state[ni,nj] == 'd':     # diamond
### Should count collected diamonds?
    state[ni,nj] = 'a'
    state[i,j] = 'p'
    agent.move([ni,nj])

  elif state[ni,nj] == 'g':     # goal
    # TODO: change state iff all diamonds are collected!!!
    state[ni,nj] = 'a'
    state[i,j] = 'p'
    agent.move([ni,nj])

  elif state[ni,nj] == 'K':     # kdoor
    if agent.has_key():
      state[ni,nj] = 'a'

  elif state[ni,nj] == 'b':     # button
    pass

  elif state[ni,nj] == 'B':     # bDoor
    pass

  else:
    print('##################### not smart #######################')

  return state

