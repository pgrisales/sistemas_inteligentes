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
# 'Q' rock over key 
# TODO: rock over key!!

# 'a' agent
# 'A' agent over spike
# '@' agent over key with key
# '_' agent over button

# Level 14, 12 & 7 are the most complex

# TODO: replace all key-agent interactions with this function
import copy
import sys

def left(pos):
  return [pos[0], pos[1] - 1] 
def right(pos):
  return [pos[0], pos[1] + 1] 
def up(pos):
  return [pos[0] - 1, pos[1]] 
def down(pos):
  return [pos[0] + 1, pos[1]] 

def possible_actions(g_state, g_level, g_goal, g_diamonds, g_finish, pos, a_key):
  l = left(pos)
  r = right(pos)
  u = up(pos)
  d = down(pos)

  actions = { 'l': l, 'r': r, 'u': u, 'd': d }
  moves = { 'l': l, 'r': r, 'u': u, 'd': d }
  for kd, v in actions.items():
    a_pos = copy.deepcopy(pos)
    key =  copy.deepcopy(a_key)
    state = copy.deepcopy(g_state)
    diamonds = copy.deepcopy(g_diamonds)
    finish = copy.deepcopy(g_finish)
    level = copy.deepcopy(g_level)
    goal = copy.deepcopy(g_goal)

  #return state, diamonds, finish, moved, (ni, nj), key
    s, d, f, moved, n_pos, k = rules(state, level, goal, diamonds, finish, pos,  v, key)
    moves[kd] = [s, actions[kd], d, f, k]
#      print('pos after: ', a2.pos)
    if not moved:
      del moves[kd]
#        print('MOVE DEL: ', k)#, actions[k]())
#        print(moves[k])
  return moves 

def key_actions(agent):
  if agent.has_key:
    moved = True
    return '@' 
  else:
    agent.has_key = True
    moved = True
    return 'a'

def rules(state, level, goal, diamonds, finish, a_pos, a_move, key):

  moved = False
  state = state
  i, j = a_pos
#  ni, nj = agent.testRules()
  ni, nj = a_move
  a_state = state[i, j]
#  print(i,j)
#  print('Entry as: ', a_state)

  wall = ['h', 'w', 'l']

  # Define wall for rock
  W = ['w', 'r', 'K', 'B', 'g']

  b = []
  B = []

  if level == 7:    #YA
    b = [(7, 2),  (12, 6)]
    B = [(8, 7),   (9, 6)]

  if level == 8:    #YA
    b = [(5, 1),  (7,8), (12,5)]
    B = [(5, 4),  (8,2), (11,7)]

  if level == 10:   #YA
    b = [(3, 7)]
    B = [(4, 6)]

  if level == 11:   #YA
    b = [(12, 5)]
    B = [(8, 2)]

  if level == 12:   #YA
    b = [(7, 5)]
    B = [(7, 4)]
    
  if level == 13:   #YA
    b = [(11, 4), (11,1), (8,4), (7,8)]
    B = [(11, 6),  (7,3), (5,7), (4,2)]

  if level == 14:   #YA
    b = [(6, 7)]
    B = [(12, 3)]

  if level == 16:   #YA
    b = [(5,7), (5,4), (9,8)]
    B = [(4,8), (5,2), (5,5)]

  if level == 17:   #YA
    b = [(6,3), (10,6), (12,3)]
    B = [(12,7), (4,8), (7,4)]

  if level == 18:   #YA
    b = [(5, 2), (10, 8)]
    B = [(5, 1), (5, 5)]

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
    moved = True
# Done
  elif (ni,nj) in B:     # bDoor
    idx = B.index((ni, nj))
    bi, bj = b[idx]
    if state[bi ,bj] != 'b':
      state[ni, nj] = 'a'
      moved = True
    else:
      state[i, j] = a_state

# Done
  elif state[ni,nj] == 'p':     # path
    state[ni,nj] = 'a'
    moved = True

# Done
  elif state[ni,nj] == 'k':     # key
    if key:
      state[ni,nj] = '@' 
      moved = True
    else:
      state[ni,nj] = 'a'
      key = True
      moved = True

# Done
  elif state[ni,nj] in wall:     # hole, wall, lava
    state[i, j] = a_state

# Done
  elif state[ni,nj] == 'd':     # diamond
    state[ni,nj] = 'a'
    moved = True
    diamonds.remove((ni, nj))

# Done
# TODO: quitar todo lo relacionado a goal, no se usa
#  elif ni == goal[0] and nj == goal[1]:     # goal
  elif state[ni,nj] == 'g':     # goal
    if len(diamonds) == 0:
      state[ni,nj] = 'a'
      moved = True
      finish = True
    else:
      state[i, j] = a_state 

# Done
  elif state[ni,nj] == 'K':     # kdoor
    if key:
      state[ni,nj] = 'a'
      moved = True
      key = False
    else:
      state[i, j] = a_state

# Done
  elif state[ni,nj] == 'r':     # rock
    nri, nrj = ni + (ni-i), nj + (nj-j)

    if state[nri, nrj] in W:
      state[i, j] = a_state

    elif state[nri, nrj] == 'l':
      state[ni, nj] = 'a'
      moved = True

    elif state[nri, nrj] == 'h':
      state[ni, nj] = 'a'
      moved = True
      state[nri, nrj] = 'p'

    elif state[nri, nrj] == 'b':
      state[ni, nj] = 'a'
      moved = True
      idx = b.index((nri, nrj))
      state[B[idx]] = 'p'
      state[nri, nrj] = 'o'

    elif state[nri, nrj] == 's':
      state[ni, nj] = 'a'
      moved = True
      state[nri, nrj] = 'R'

    elif state[nri, nrj] == 'k': 
      state[ni, nj] = 'a'
      moved = True
      state[nri, nrj] = 'Q'
      
    elif state[nri, nrj] == 'd':
      state[ni, nj] = 'a'
      moved = True
      state[nri, nrj] = 'D'

    else:
      state[ni, nj] = 'a'
      moved = True
      state[nri, nrj] = 'r'

# Done I think!
  elif state[ni,nj] == 'Q':     # rock over key
    nri, nrj = ni + (ni-i), nj + (nj-j)

    if state[nri, nrj] in W:
      state[i, j] = a_state

    elif state[nri, nrj] == 'l':
      if key:
        state[ni,nj] = '@' 
        moved = True
      else:
        state[ni,nj] = 'a'
        key = True
        moved = True

    elif state[nri, nrj] == 'h':
      if key:
        state[ni,nj] = '@' 
        moved = True
      else:
        state[ni,nj] = 'a'
        key = True
        moved = True
      state[nri, nrj] = 'p'

    elif state[nri, nrj] == 'b':
      if key:
        state[ni,nj] = '@' 
        moved = True
      else:
        state[ni,nj] = 'a'
        key = True
        moved = True
      idx = b.index((nri, nrj))
      state[B[idx]] = 'p'
      state[nri, nrj] = 'o'

    elif state[nri, nrj] == 's':
      if key:
        state[ni,nj] = '@' 
        moved = True
      else:
        state[ni,nj] = 'a'
        key = True
        moved = True
      state[nri, nrj] = 'R'

    elif state[nri, nrj] == 'k': 
      if key:
        state[ni,nj] = '@' 
        moved = True
      else:
        state[ni,nj] = 'a'
        key = True
        moved = True
      state[nri, nrj] = 'Q'
      
    elif state[nri, nrj] == 'd':
      if key:
        state[ni,nj] = '@' 
        moved = True
      else:
        state[ni,nj] = 'a'
        key = True
        moved = True
      state[nri, nrj] = 'D'

    else:
      if key:
        state[ni,nj] = '@' 
        moved = True
      else:
        state[ni,nj] = 'a'
        key = True
        moved = True
      state[nri, nrj] = 'r'

# Done
  elif state[ni,nj] == 'R':     # rock over spike 
    nri, nrj = ni + (ni-i), nj + (nj-j)

    if state[nri, nrj] in W:
      state[i, j] = a_state

    elif state[nri, nrj] == 'l':
      state[ni, nj] = 'A'
      moved = True

    elif state[nri, nrj] == 'h':
      state[ni, nj] = 'A'
      moved = True
      state[nri, nrj] = 'p'

    elif state[nri, nrj] == 'b':
      state[ni, nj] = 'A'
      moved = True
      idx = b.index((nri, nrj))
      state[B[idx]] = 'p'
      state[nri, nrj] = 'o'

    elif state[nri, nrj] == 's':
      state[ni, nj] = 'A'
      moved = True
      state[nri, nrj] = 'R'
      
    elif state[nri, nrj] == 'd':
      state[ni, nj] = 'A'
      moved = True
      state[nri, nrj] = 'D'

    elif state[nri, nrj] == 'k': 
      state[ni, nj] = 'A'
      moved = True
      state[nri, nrj] = 'Q'

    else:
      state[ni, nj] = 'a'
      moved = True
      state[nri, nrj] = 'r'

# Done
  elif state[ni,nj] == 'o':     # rock over button
    nri, nrj = ni + (ni-i), nj + (nj-j)

    if state[nri, nrj] in W:
      state[i, j] = a_state

    elif state[nri, nrj] == 'l':
      state[ni, nj] = '_'
      moved = True

    elif state[nri, nrj] == 'h':
      state[ni, nj] = '_'
      moved = True
      idx = b.index((ni, nj))
      state[B[idx]] = 'p'
      state[nri, nrj] = 'p'

    elif state[nri, nrj] == 'b':
      state[ni, nj] = '_'
      moved = True
      idx = b.index((nri, nrj))
      state[B[idx]] = 'p'
      state[nri, nrj] = 'o'

    elif state[nri, nrj] == 's':
      state[ni, nj] = '_'
      moved = True
      state[nri, nrj] = 'R'
      
    elif state[nri, nrj] == 'd':
      state[ni, nj] = '_'
      moved = True
      state[nri, nrj] = 'D'

    elif state[nri, nrj] == 'k': 
      state[ni, nj] = '_'
      moved = True
      state[nri, nrj] = 'Q'

    else:
      state[ni, nj] = 'a'
      moved = True
      state[nri, nrj] = 'r'

# Done
  elif state[ni,nj] == 'D':     # rock over diamond
    nri, nrj = ni + (ni-i), nj + (nj-j)

    if state[nri, nrj] in W:
      state[i, j] = a_state

    elif state[nri, nrj] == 'l':
      state[ni, nj] = 'a'
      moved = True
      diamonds.remove((ni, nj))

    elif state[nri, nrj] == 'h':
      state[ni, nj] = 'a'
      moved = True
      diamonds.remove((ni, nj))
      state[nri, nrj] = 'p'

    elif state[nri, nrj] == 'b':
      state[ni, nj] = 'a'
      moved = True
      diamonds.remove((ni, nj))
      idx = b.index((nri, nrj))
      state[B[idx]] = 'p'
      state[nri, nrj] = 'o'

    elif state[nri, nrj] == 's':
      state[ni, nj] = 'a'
      moved = True
      diamonds.remove((ni, nj))
      state[nri, nrj] = 'R'
      
    elif state[nri, nrj] == 'd':
      state[ni, nj] = 'a'
      moved = True
      diamonds.remove((ni, nj))
      state[nri, nrj] = 'D'

    elif state[nri, nrj] == 'k': 
      state[ni, nj] = 'a'
      moved = True
      diamonds.remove((ni, nj))
      state[nri, nrj] = 'Q'

    else:
      state[ni, nj] = 'a'
      moved = True
      diamonds.remove((ni, nj))
      state[nri, nrj] = 'r'

# Done
  elif state[ni,nj] == 'b':     # button
    state[ni, nj] = '_'
    moved = True
    idx = b.index((ni, nj))
    state[B[idx]] = 'p'


  else:
    print('##################### rules not working #######################')

  return state, diamonds, finish, moved, (ni, nj), key
# rules(state, diamonds, finish, a_pos, a_move, key)
