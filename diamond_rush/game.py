import numpy as np
import copy
from agent import Agent
from rules import rules

# Levels with buttons: 8, 9, 11, 12, 13, 14, 15, 17, 18, 19
class Game:
  def __init__(self, level, a_pos):
    self.level = level 
    self.a_pos = a_pos
    self.state = self.load_level(self.level, self.a_pos)
    self.diamonds = self.diamonds_pos(self.state)
    self.g_pos = self.goal_pos(self.state)
    self.finish = False

  def load_level(self, level, a_pos): 
    state = np.loadtxt('./levels/default_init_states/' + str(level), dtype=str)

    if a_pos != self.agent_pos(state):
      # TODO: Done?
      state[self.agent_pos(state)] = 'p'
      state[a_pos] = 'a'
      return state

    return state

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

  def left(self, pos):
    return [pos[0], pos[1] - 1] 
  def right(self, pos):
    return [pos[0], pos[1] + 1] 
  def up(self, pos):
    return [pos[0] - 1, pos[1]] 
  def down(self, pos):
    return [pos[0] + 1, pos[1]] 

#  s, d, f, moved, n_pos, k = rules(state, level, diamonds, finish, pos,  v, key)
#  def possible_actions(self, agent, game):
  def possible_actions(self, state, level, diamonds, finish, pos, key):
#    a_pos = agent.pos
#    key =  agent.has_key
#    state = game.state
#    diamonds = game.diamonds
#    finish = game.finish
#    level = game.level

    l = self.left(pos)
    r = self.right(pos)
    u = self.up(pos)
    d = self.down(pos)

    actions = { 'l': l, 'r': r, 'u': u, 'd': d }
    moves = { 'l': l, 'r': r, 'u': u, 'd': d }
    for kd, v in actions.items():
      a_pos = copy.deepcopy(pos)
      key =  copy.deepcopy(key)
      state = copy.deepcopy(state)
      diamonds = copy.deepcopy(diamonds)
      finish = copy.deepcopy(finish)
      level = copy.deepcopy(level)
#      a2 = copy.deepcopy(agent)
#      g2 = copy.deepcopy(game)
#      key =  a2.has_key
#      pos = a2.pos
#      state = g2.state
#      diamonds = g2.diamonds
#      finish = g2.finish
#      level = g2.level
#      print('must not change: ', game.state)
#      print('must not change: ', state)
#      print(' move: ', k)
#      print('pos bf: ', a2.pos)
      s, d, f, moved, n_pos, k = rules(state, level, diamonds, finish, a_pos,  v, key)
#      print('pos after: ', a2.pos)
      if not moved:
        del moves[kd]
#        print('MOVE DEL: ', k)#, actions[k]())
#        print(moves[k])
    return moves 

  def play(self):
    pass

