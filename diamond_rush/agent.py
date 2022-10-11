#!/usr/bin/env python3
class Agent:
  def __init__(self, agent_pos):
    self.agent_pos = agent_pos 
    self.hasKey = False

  def compute(self):
    pass

  def hasKey(self):
    return self.hasKey

  def set_hasKey(self, hasKey):
    self.hasKey = hasKey

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

agent = Agent([1,1])
print(agent.get_pos())
agent.left()
print(agent.get_pos())

