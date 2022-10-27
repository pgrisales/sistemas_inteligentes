#!/usr/bin/env python3
import numpy as np

class Agent:
  def __init__(self, agent_pos):
    self.pos = agent_pos 
    self.has_key = False

  def compute(self):
    from random import randint
    i  = randint(0,3)
    d = ['l', 'r', 'u', 'd']
    if d[i] == 'l':
      return self.left()
    elif d[i] == 'r':
      return self.right()
    elif d[i] == 'u':
      return self.up()
    elif d[i] == 'd':
      return self.down()

  def play(self, state):
    i, j = self.compute()
    while state[i, j] == 'w' or state[i, j] == 'l':
      i, j = self.compute()
    assert state[i,j] != 'w'
    assert state[i,j] != 'l'
    return i, j 

  def left(self):
    return [self.pos[0], self.pos[1] - 1] 
  def right(self):
    return [self.pos[0], self.pos[1] + 1] 
  def up(self):
    return [self.pos[0] - 1, self.pos[1]] 
  def down(self):
    return [self.pos[0] + 1, self.pos[1]] 


"""
#l0 = 'rrrrrdddlllllddrdrrrrd'
l11 = 'ulrrdllddrdrrurddrruudddduullrlullllddddrrrrlrllllddrrrruuurrurldlldddrrrllluuuurdruuuuddlldddrlddrruuuuuuuuulll'
a = Agent((1,1))
print(a.has_key)
a.has_key = True
print(a.has_key)
l11 = [((12,5),(8,2))]
b = [(12,5),(1,1),(1,3)]
B = [(8,2),(2,2),(3,3)]
idx = b.index((12,5))

state = np.loadtxt('./levels/default_init_states/11', dtype=str)

print(state[B[idx]])
print(state[8, 2])
#print(b.index((1,1)))
"""
