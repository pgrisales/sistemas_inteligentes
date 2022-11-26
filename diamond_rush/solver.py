#!/usr/bin/env python3
import copy
from a_star import a_star
from game import buttons_pos, holes_pos, keys_pos, rocks_pos
import sys

from itertools import permutations

class State:
  def __init__(path=None, state=None, goals=None, finish=None, pos=None, key=None, trap=None):
    self.path = path
    self.state = state
    self.goals = goals 
    self.finish = finish
    self.pos = pos
    self.key = key
    self.trap = trap

class Goal:
  def __init__(self, pos, h, type_char):
    self.pos = pos
    self.h = h
    self.h2 = 0
    self.type = type_char
    self.trap = False

  def __eq__(self, other):
    return self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]

def h(src, goal):
  return abs(src[0] - goal[0]) +  abs(src[1] - goal[1])  

def set_goals_holes(pos, holes):
  goals = []
  for idx, i in enumerate(holes):
    new_h = h(pos, i)
    nd = Goal(i, new_h, 'h')
    goals.append(nd)
    for j in range(idx):
      if goals[idx].h < goals[j].h:
        goals[idx], goals[j] = goals[j], goals[idx]
  
  return goals

def set_goals_keys(pos, keys):
  goals = []
  for idx, i in enumerate(keys):
    new_h = h(pos, i)
    nd = Goal(i, new_h, 'k')
    goals.append(nd)
    for j in range(idx):
      if goals[idx].h < goals[j].h:
        goals[idx], goals[j] = goals[j], goals[idx]
  
  return goals

def set_goals_buttons(pos, buttons):
  goals = []
  for idx, i in enumerate(buttons):
    new_h = h(pos, i)
    nd = Goal(i, new_h, 'b')
    goals.append(nd)
    for j in range(idx):
      if goals[idx].h < goals[j].h:
        goals[idx], goals[j] = goals[j], goals[idx]
  
  return goals

def set_goals_diamonds(pos, diamonds):
  goals = []
  for idx, i in enumerate(diamonds):
    new_h = h(pos, i)
    nd = Goal(i, new_h, 'd')
    goals.append(nd)
    for j in range(idx):
      if goals[idx].h < goals[j].h:
        goals[idx], goals[j] = goals[j], goals[idx]
  
  return goals

def set_priority(agent, *args):
  goals = []
  for goal in args:
    for idx, i in enumerate(goal):
      goals.append(i)

      if i.type == 'd':
        i.h += h(agent.pos, i.pos) + i.h2
      elif i.type == 'k':
        i.h += h(agent.pos, i.pos) + i.h2
        if agent.has_key:
          i.h += 10
      elif i.type == 'b':
        i.h += h(agent.pos, i.pos) + i.h2 + 8
      elif i.type == 'h':
        i.h += h(agent.pos, i.pos) + i.h2 + 8
      for j in range(idx):
        if goals[idx].h < goals[j].h:
            goals = goals[:j] + [goals[j]] + goals[j:]

  return goals

def update_priority(a, g, goals):
  discarted = get_goals(a, g)
  update = []

  for g in goals:
    for g2 in discarted:
#      print(len(discarted))
      if g.pos == g2.pos:
        update.append(g)
        discarted.remove(g2)
        continue

  for idx, i in enumerate(update):
    if i.type == 'd':
      if h(a.pos, i.pos) < 3:
        i.h = 3
      else:
        i.h += h(a.pos, i.pos) + i.h2
    elif i.type == 'k':
      if h(a.pos, i.pos) < 3:
        i.h = 3
      else:
        i.h += h(a.pos, i.pos) + i.h2
      if a.has_key:
        i.h += 10
    elif i.type == 'b':
      i.h += h(a.pos, i.pos) + i.h2 + 8
    elif i.type == 'h':
      i.h += h(a.pos, i.pos) + i.h2 + 8

    for j in range(idx):
      if update[idx].h < update[j].h:
        update[j], update[idx] = update[idx], update[j]
#        update = update[:j] +[update[idx]] + update[idx:]
  return update

def new_order(goals, n):
  if n:
    for i in goals:
      for j in n:
        if j == i:
          j.h = i.h
  else:
    for i in goals:
      n.append(i)

  return n

def get_goals(a, g):
  diamonds= set_goals_diamonds(a.pos, g.diamonds)
  keys = set_goals_keys(a.pos, keys_pos(g.state))
  holes = set_goals_holes(a.pos, holes_pos(g.state))
  buttons = set_goals_buttons(a.pos, buttons_pos(g.state))
#  rocks = rocks_pos(g.state) # Not sure its needed here

  goals = set_priority(a, diamonds, keys, holes, buttons)

  return goals

def solver(game, agent) :
  a = copy.deepcopy(agent)
  g = copy.deepcopy(game)
  
#  goals_copy = copy.deepcopy(g.diamonds)
  solution = []
  perm = []

  goals = get_goals(a, g)
  new_g = []

  count = 0
  idx = 0
  a = [1,2,3,4,5,6,7,8,9,10]
  p = permutations(a)
#  p = permutations(goals)
  for idx, i in enumerate(list(p)):
    print(idx, i)
  sys.exit('carnal')
#  while len(goals) > 0 or g.finish:
#    count += 1
#    print('count: ', count)
#    if count % 15 == 0:
#      print('######################### Game Reset ##############################')
#      a = copy.deepcopy(agent)
#      g = copy.deepcopy(game)
#      solution = []
##      goals = get_goals(a, g)
#      goals = new_g
#      goals = update_priority(a, g, goals)
#      idx = 0
#      if count == 30000:
#        sys.exit('puta')
#
#    i = goals[idx]
#
#    print('agent position: ', a.pos)
#    print('Objetivo: ', i.pos, i.h)
#    print()
#    new_g = new_order(goals, new_g)
#
#    path, g.state, g.diamonds, g.finish, a.pos, a.has_key, trap = a_star(g, a, i.pos)
#    
##    print(path)
#    print()
#    print('len of goals bef: ', len(goals))
#    for i in goals:
#      print('######################### goals Antes de la reasig ##############################')
#      print(i.pos, i.h, i.type)
#    print()
#    if len(path) > 0:
#      if not trap:
#        new_g = new_order(goals, new_g)
#        del goals[idx]
##        goals.remove(idx)
#      else:
##        print(goals[idx].pos, goals[idx].h)
#        goals[idx].h += 100//(idx+1)
#        trap = False
##        print(goals[idx].pos, goals[idx].h)
##        sys.exit('trap')
##        idx += 1
##      goals = set_goals_diamonds(a.pos, g.diamonds)
#
#      print('NEW pos', a.pos)
##      goals = set_goals_diamonds(a.pos, g.diamonds)
##      goals = set_p(a.pos, goals)
#      #goals = get_goals(a, g)
#      goals = update_priority(a, g, goals)
#      solution.append(path[1:])
#      print()
## if trap dont remove for permutations 
#    else:
#      print(a.pos)
#      if len(goals) > idx:
#        print('SWAP DONE')
#        goals[idx].h += 100//(idx+1)
#        goals = update_priority(a, g, goals)
##        goals = get_goals(a, g)
##        idx = 0
##        solution = []
#
#    print()
#
#  fp, s, d, f, pos, key, trap = a_star(g, a, game.g_pos)
#  solution.append(fp[1:])

  return solution

def try_perm(goals, a, g):
  return solution, goals
