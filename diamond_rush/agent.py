#!/usr/bin/env python3
class Agent:
  def __init__(self, agent_pos):
    self.agent_pos = agent_pos 
    self.key = False

  def compute(self):
    from random import randint
    i  = randint(0,3)
    d = [0,1,2,3,4]
    if d[i] == 0:
      return self.left()
    elif d[i] == 1:
      return self.right()
    elif d[i] == 2:
      return self.up()
    elif d[i] == 3:
      return self.down()

  def play(self, state):
    i, j = self.compute()
    while state[i, j] == 'w' or state[i, j] == 'l':
      i, j = self.compute()
    assert state[i,j] != 'w'
    assert state[i,j] != 'l'
    return i, j 

  def has_key(self):
    return self.key

  def set_has_key(self, key):
    self.key = key 

  def get_pos(self):
    return self.agent_pos

  def move(self, new_pos): 
    self.agent_pos = new_pos

  def left(self):
    return [self.agent_pos[0], self.agent_pos[1] - 1] 
  def right(self):
    return [self.agent_pos[0], self.agent_pos[1] + 1] 
  def up(self):
    return [self.agent_pos[0] - 1, self.agent_pos[1]] 
  def down(self):
    return [self.agent_pos[0] + 1, self.agent_pos[1]] 

def setGoals():
  pass

"""
agent = Agent([1,1])
print(agent.get_pos())
agent.left()
print(agent.get_pos())
"""
