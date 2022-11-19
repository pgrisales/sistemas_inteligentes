#!/usr/bin/env python3
import numpy as np
import copy
from a_star import a_star

def solver(game, agent):
  a2 = copy.deepcopy(agent)
  g2 = copy.deepcopy(game)
  print(g2.diamonds[0])
  a_star(g2, a2, g2.diamonds[0])

