import numpy as np
from agent import Agent

# Levels with buttons: 8, 9, 11, 12, 13, 14, 15, 17, 18, 19
class Game:
  def __init__(self, level, a_pos):
    self.level = level 
    self.a_pos = a_pos
    self.state = self.load_level(self.level, self.a_pos)
    self.diamonds = self.diamonds_pos(self.state)
    self.g_pos = self.goal_pos()
    self.finish = False

  def load_level(self, level, a_pos): 
    state = np.loadtxt('./levels/default_init_states/' + str(level), dtype=str)

    if a_pos != self.agent_pos(state):
      # TODO: Done?
      state[self.agent_pos(state)] = 'p'
      state[a_pos] = 'a'
      return state

    return state

  def goal_pos(self):
    for i in range(len(self.state)):
      for j in range(len(self.state[0])):
        if self.state[i,j] == 'g':
          return (i, j)

  def rocks_pos(self, state):
    pos = []
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'r' or state[i,j] == 'R' or state[i,j] == 'o' or state[i,j] == 'D' or state[i,j] == 'Q':
          pos.append((i,j))
    return pos 

  def holes_pos(self, state):
    pos = []
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'h':
          pos.append((i,j))
    return pos 

  def buttons_pos(self, state):
    pos = []
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'b' or state[i,j] == '_':
          pos.append((i,j))
    return pos 

  def diamonds_pos(self, state):
    pos = []
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'd' or state[i,j] == 'D':
          pos.append((i,j))
    return pos 

  def agent_pos(self, state):
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'a' or state[i,j] == 'A' or state[i,j] == '@' or state[i,j] == '_':
          return i,j

  def play(self):
    pass

