#!/usr/bin/env python3
import copy
from a_star import a_star

class Diamond:
  def __init__(self, pos, h):
    self.pos = pos
    self.h = h

def h(src, goal):
  return abs(src[0] - goal[0]) +  abs(src[1] - goal[1])  

# set diamond priority -> agent_pos, diamonds[]
def i_p(pos, d):
  diamonds = []
  for idx, i in enumerate(d):
    nh = h(pos, i)
    nd = Diamond(i, nh)
    diamonds.append(nd)
    for j in range(idx):
      if diamonds[idx].h < diamonds[j].h:
        diamonds[idx], diamonds[j] = diamonds[j], diamonds[idx]
  
  return diamonds

def set_p(pos, d):
  for idx, i in enumerate(d):
    i.h = h(pos, i.pos)
    for j in range(idx):
      if d[idx].h < d[j].h:
        d[idx], d[j] = d[j], d[idx]
  
  return d

def solver(game, agent):
  a = copy.deepcopy(agent)
  g = copy.deepcopy(game)

  solution = []
  diamonds = i_p(a.pos, g.diamonds)
  #for i in diamonds:
  #  print(i.pos, i.h)
  while len(diamonds) > 0:
    i = diamonds[0]
    print('Objetivo: ', i.pos, i.h)
    path, g.state, g.diamonds, g.finish, a.pos, a.key  = a_star(g, a, i.pos)

    diamonds.remove(i)
### check if pos diamonds has been already visited TODO: improve this 
    for x in solution:
      for z in x:
        for d in diamonds:
          if z[1] in d.pos:
            diamonds.remove(d)
        print('Rest: ', d.pos, d.h)
    diamonds = set_p(a.pos, diamonds)
    solution.append(path[1:])
    print('agent position: ', a.pos)
    print('Diamond goal: ', i.pos)
    for j in path[1:]:
      print(j)

  g.diamonds = diamonds
  fp, s, d, f, pos, key = a_star(g, a, game.g_pos)
  print(fp[1:])
  solution.append(fp[1:])

  return solution

