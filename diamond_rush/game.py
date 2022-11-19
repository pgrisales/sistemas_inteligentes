import numpy as np
import copy
from agent import Agent
from rules import rules

# Levels with buttons: 8, 9, 11, 12, 13, 14, 15, 17, 18, 19
class Game:
  def __init__(self, level, a_pos):
    self.level = level 
    self.a_pos = a_pos
    self.state, self.f_state = self.load_level(self.level, self.a_pos)
    self.diamonds = self.diamonds_pos(self.state)
    self.g_pos = self.goal_pos(self.state)
    self.finish = False

  def load_level(self, level, a_pos): 
    state = np.loadtxt('./levels/default_init_states/' + str(level), dtype=str)
    f_state = np.loadtxt('./levels/final_states/' + str(level), dtype=str)

    if a_pos != self.agent_pos(state):
      # TODO: Done?
      state[self.agent_pos(state)] = 'p'
      state[a_pos] = 'a'
      return state, f_state

    return state, f_state

  def goal_pos(self, state):
    for i in range(len(state)):
      for j in range(len(state[0])):
        if state[i,j] == 'g':
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

  def possible_actions(self, agent, game):
    moves = copy.copy(agent.actions)
    for k, v in agent.actions.items():
      a2 = copy.deepcopy(agent)
      g2 = copy.deepcopy(game)
#      print(' move: ', k)
#      print('pos bf: ', a2.pos)
      rules(a2, moves[k](), g2)
#      print('pos after: ', a2.pos)
      if agent.pos == a2.pos:
#        print('MOVE DEL: ', moves[k]())
        del moves[k]
    return moves 

  def play(self):
    pass

