#!/usr/bin/env python3
import cv2 
import numpy as np
import os
from agent import Agent
from game import *

class Enviroment:
  def __init__(self):
    pass
  def run(self):
    i = [5,2]
    tempL = './levels/1.png'
    level = Level(tempL,i)
    agent = Agent(i)
    i = 1
    while not np.array_equal(level.get_state(), level.get_f_state()):
      print(level.new_state(agent))
      
      print('##### ', agent.get_pos(), ' ####')
      print('##### ', i, ' ####')
      i += 1

#env = Enviroment()
#env.run()
