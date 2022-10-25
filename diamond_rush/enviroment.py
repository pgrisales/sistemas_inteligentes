#!/usr/bin/env python3
import cv2 
import numpy as np
import os
from agent import Agent
from game import *

### manage interactions btw Level and Agent... and it captures image of enviroment, dk if rules goes here or in level
class Enviroment:
  ### TODO: check if agent has change pos, add metadata of levels as txt... add rules
  ### TODO probably need to remember 2 states back for spikes and some rocks interactions...
  def __init__(self):
    pass
  def run(self):
    i = [5,2] # Default init pos level 0
    tempL = './levels/1.png'
    level = Level(tempL,i)
    agent = Agent(i)
#    for i in range(3):
#      print(level.get_state())
#      print(agent.get_pos())
#      print()
#      level.new_state(agent, agent.play())
    i = 1
    while not np.array_equal(level.get_state(), level.get_f_state()):
      print(level.new_state(agent))
      #print(level.get_state())
      
      print('##### ', agent.get_pos(), ' ####')
      print('##### ', i, ' ####')
      i += 1

#env = Enviroment()
#env.run()
"""
i = [5,2] # Default init pos level 0
level = Level(1,i)
agent = Agent(i)
a = agent.play()
print(a[0])
print(level.get_state())
print('pos ', level.agent_pos(level.get_state()))
print()
l = [0,-1]
#print(l[1])
print(level.new_state(l))
print('new pos ', level.agent_pos(level.get_state()))
"""
