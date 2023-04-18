import numpy as np
from agent import Agent

# Levels with buttons: 8, 9, 11, 12, 13, 14, 15, 17, 18, 19
class Game:
  def __init__(self, level, a_pos):
    self.level = level 
    self.a_pos = a_pos
    self.state = self.load_level(self.level, self.a_pos)
    self.diamonds = diamonds_pos(self.state)
    self.g_pos = goal_pos(self.state)
    self.finish = False

  def load_level(self, level, a_pos): 
    state = np.loadtxt('./levels/default_init_states/' + str(level), dtype=str)

    if a_pos != agent_pos(state):
      state[agent_pos(state)] = 'p'
      state[a_pos] = 'a'
      return state

    return state

  def play(self):
    pass

def goal_pos(state):
  for i in range(len(state)):
    for j in range(len(state[0])):
      if state[i,j] == 'g':
        return (i, j)

def rocks_pos(state):
  pos = []
  for i in range(len(state)):
    for j in range(len(state[0])):
      if state[i,j] == 'r' or state[i,j] == 'R' or state[i,j] == 'o' or state[i,j] == 'D' or state[i,j] == 'Q':
        pos.append((i,j))
  return pos 

def holes_pos(state):
  pos = []
  for i in range(len(state)):
    for j in range(len(state[0])):
      if state[i,j] == 'h':
        pos.append((i,j))
  return pos 

def lava_pos(state):
  pos = []
  for i in range(len(state)):
    for j in range(len(state[0])):
      if state[i,j] == 'l':
        pos.append((i,j))
  return pos 

def buttons_pos(state):
  pos = []
  for i in range(len(state)):
    for j in range(len(state[0])):
      if state[i,j] == 'b' or state[i,j] == '_':
        pos.append((i,j))
  return pos 

def diamonds_pos(state):
  pos = []
  for i in range(len(state)):
    for j in range(len(state[0])):
      if state[i,j] == 'd' or state[i,j] == 'D':
        pos.append((i,j))
  return pos 

def kDoor_pos(state):
  pos = []
  for i in range(len(state)):
    for j in range(len(state[0])):
      if state[i,j] == 'K':
        pos.append((i,j))
  return pos 

def keys_pos(state):
  pos = []
  for i in range(len(state)):
    for j in range(len(state[0])):
      if state[i,j] == 'k':
        pos.append((i,j))
  return pos 

def agent_pos(state):
  for i in range(len(state)):
    for j in range(len(state[0])):
      if state[i,j] == 'a' or state[i,j] == 'A' or state[i,j] == '@' or state[i,j] == '_':
        return i,j


