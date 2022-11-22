#!/usr/bin/env python3
import copy
from a_star import a_star
from game import buttons_pos, holes_pos 

import sys

class Goal:
  def __init__(self, pos, h):
    self.pos = pos
    self.h = h
    self.h2 = 0
    self.trap = False

def h(src, goal):
  return abs(src[0] - goal[0]) +  abs(src[1] - goal[1])  

# set diamond priority -> agent_pos, diamonds[]
def i_p(pos, d):
  goals = []
  for idx, i in enumerate(d):
    nh = h(pos, i)
    nd = Goal(i, nh)
    goals.append(nd)
    for j in range(idx):
      if goals[idx].h < goals[j].h:
        goals[idx], goals[j] = goals[j], goals[idx]
  
  return goals

def set_p(pos, d):
  for idx, i in enumerate(d):
    i.h = h(pos, i.pos) 
    i.h += i.h2
    for j in range(idx):
      if d[idx].h < d[j].h:
        d[idx], d[j] = d[j], d[idx]
  
  return d

class State:
  def __init__(path=None, state=None, goals=None, finish=None, pos=None, key=None, trap=None):
    self.path = path
    self.state = state
    self.goals = goals 
    self.finish = finish
    self.pos = pos
    self.key = key
    self.trap = trap

def solver(game, agent) :
  a = copy.deepcopy(agent)
  g = copy.deepcopy(game)

  solution = []
  perm = []
  goals = i_p(a.pos, g.diamonds)
  #for i in diamonds:
  #  print(i.pos, i.h)
  count = 0
  idx = 0
  while len(goals) > 0:
    count += 1
    if count == 40:
      break
    i = goals[idx]

    print('agent position: ', a.pos)
    print('Objetivo: ', i.pos, i.h)
    print()

    path, g.state, g.diamonds, g.finish, a.pos, a.key, trap = a_star(g, a, i.pos)
    
    if len(path) > 0:
      if not trap:
        print(trap, i.pos, 'trap in pos')
        goals.remove(i)
#      else:
#        goals[idx].h2 += 10*(idx+1)
#        idx += 1
#      goals = i_p(a.pos, g.diamonds)

      print('NEW pos', a.pos)
      goals = i_p(a.pos, g.diamonds)
      goals = set_p(a.pos, goals)
      solution.append(path[1:])
      print()
      for i in goals:
        print('goals restantes')
        print(i.pos, i.h)
      print()
# if trap dont remove for permutations 
    else:
      print(a.pos)
      if len(goals) > idx:
        print('SWAP DONE')
        print(a.key)
        for i in goals:
          print('goals restantes')
          print(i.pos, i.h)
        print()
        goals[idx].h2 += 10
        goals = set_p(a.pos, goals)
#        idx = 0
#        solution = []

    print()

  fp, s, d, f, pos, key, trap = a_star(g, a, game.g_pos)
  solution.append(fp[1:])

  return solution

def try_perm(goals, a, g):
  return solution, goals
