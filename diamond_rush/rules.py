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

def rules(agent: Agent, game: Game):
  state = game.state
  i, j = agent.pos
  ni, nj = agent.play(state)
  a_state = state[i, j]
  wall = ['h', 'w', 'l']

  b = []
  B = []
  if game.level = 11
    b = [(12,5)]
    B = [(8,2)]

  if a_state == 'a':
    state[i, j] = 'p'
    
  elif a_state == 'A':
    state[i, j] = 'w'

  elif a_state == '_':
    state[i, j] = 'b'

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
    if agent.has_key:
      state[ni,nj] = '@' 
    else:
      state[ni,nj] = 'a'
      agent.has_key = True

# Done
  elif state[ni,nj] in wall:     # hole, wall, lava
    state[i, j] = a_state

# Done
  elif state[ni,nj] == 'd':     # diamond
    state[ni,nj] = 'a'
    agent.pos = (ni, nj)
    game.diamonds.remove((ni, nj))

# Done
  elif state[ni,nj] == 'g':     # goal
    if len(game.diamonds) == 0:
      state[ni,nj] = 'a'
      agent.pos = (ni, nj)
      game.finish = True
    else:
      state[i, j] = a_state 

# Done
  elif state[ni,nj] == 'K':     # kdoor
    if agent.has_key:
      state[ni,nj] = 'a'
    else:
      state[i, j] = a_state

# Done
  elif state[ni,nj] == 'r':     # rock
    nri, nrj = ni + (ni-i), nj + (nj-j)
    w = ['w','r','K','B']

    if state[nri, nrj] in w:
      state[i, j] = a_state

    elif state[nri, nrj] == 'l':
      state[ni, nj] = 'a'

    elif state[nri, nrj] == 'b':
      state[ni, nj] = 'a'
      idx = b.index((nri, nrj))
      state[B[idx]] = 'p'
      state[nri, nrj] = 'o'

    elif state[nri, nrj] == 's':
      state[ni, nj] = 'a'
      state[nri, nrj] = 'R'
      
    elif state[nri, nrj] == 'd':
      state[ni, nj] = 'a'
      state[nri, nrj] = 'R'

# Done
  elif state[ni,nj] == 'R':     # rock over spike 
    nri, nrj = ni + (ni-i), nj + (nj-j)
    w = ['w','r','K','B']

    if state[nri, nrj] in w:
      state[i, j] = a_state

    elif state[nri, nrj] == 'l':
      state[ni, nj] = 'a'

    elif state[nri, nrj] == 'b':
      state[ni, nj] = 'a'
      idx = b.index((nri, nrj))
      state[B[idx]] = 'p'
      state[nri, nrj] = 'o'

    elif state[nri, nrj] == 's':
      state[ni, nj] = 'a'
      state[nri, nrj] = 'R'
      
    elif state[nri, nrj] == 'd':
      state[ni, nj] = 'a'
      state[nri, nrj] = 'R'

# Done
  elif state[ni,nj] == 'o':     # rock over button
    nri, nrj = ni + (ni-i), nj + (nj-j)
    w = ['w','r','K','B']

    if state[nri, nrj] in w:
      state[i, j] = a_state

    elif state[nri, nrj] == 'l':
      state[ni, nj] = 'a'

    elif state[nri, nrj] == 'b':
      state[ni, nj] = 'a'
      idx = b.index((nri, nrj))
      state[B[idx]] = 'p'
      state[nri, nrj] = 'o'

    elif state[nri, nrj] == 's':
      state[ni, nj] = 'a'
      state[nri, nrj] = 'R'
      
    elif state[nri, nrj] == 'd':
      state[ni, nj] = 'a'
      state[nri, nrj] = 'R'

# Done
  elif state[ni,nj] == 'D':     # rock over diamond
    nri, nrj = ni + (ni-i), nj + (nj-j)
    w = ['w','r','K','B']

    if state[nri, nrj] in w:
      state[i, j] = a_state

    elif state[nri, nrj] == 'l':
      state[ni, nj] = 'a'
      game.diamonds.remove((ni, nj))

    elif state[nri, nrj] == 'b':
      state[ni, nj] = 'a'
      game.diamonds.remove((ni, nj))
      idx = b.index((nri, nrj))
      state[B[idx]] = 'p'
      state[nri, nrj] = 'o'

    elif state[nri, nrj] == 's':
      state[ni, nj] = 'a'
      game.diamonds.remove((ni, nj))
      state[nri, nrj] = 'R'
      
    elif state[nri, nrj] == 'd':
      state[ni, nj] = 'a'
      game.diamonds.remove((ni, nj))
      state[nri, nrj] = 'R'

# Done
  elif state[ni,nj] == 'b':     # button
    state[ni, nj] = '_'
    idx = b.index((ni, nj))
    state[B[idx]] = 'p'

# Done
  elif state[ni,nj] == 'B':     # bDoor
    idx = B.index((ni, nj))
    bi, bj = b[idx]
    if state[bi ,bj] != 'b':
      state[ni, nj] = 'a'
    else:
      state[i, j] = a_state

  else:
    print('##################### not smart #######################')

  return state

