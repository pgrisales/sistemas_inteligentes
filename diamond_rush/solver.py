#!/usr/bin/env python3
import copy
from a_star import a_star
from game import buttons_pos, holes_pos, keys_pos, rocks_pos
import sys

class Goal:
  def __init__(self, pos, h, type_char, agent=None, game=None, parent=None, childs=[], visited= set()):
    self.pos = pos
    self.h = h
    self.h2 = 0
    self.type = type_char
    self.trap = False
    self.parent = parent
    self.childs = childs
    self.visited = visited
    self.path = []
    self.agent = agent
    self.game = game

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

def get_goals(a, g):
  diamonds= set_goals_diamonds(a.pos, g.diamonds)
  keys = set_goals_keys(a.pos, keys_pos(g.state))
  holes = set_goals_holes(a.pos, holes_pos(g.state))
  buttons = set_goals_buttons(a.pos, buttons_pos(g.state))
#  rocks = rocks_pos(g.state) # Not sure its needed here

  goals = set_priority(a, diamonds, keys, holes, buttons)
  return goals

count = 0
def make_path(agent, game, src, goals, visited_trap=set()):
  global count
  count += 1
  print(count)
  a = copy.deepcopy(agent)
  g = copy.deepcopy(game)

  solution = []
  idx = 0
  
  goals = copy.deepcopy(goals)

  print()
  for z in goals:
    print(z.pos, z.h)
  print('---------------------- still to getem --------------------------------')

  while not g.finish:
    if len(goals) == 0:
      solution = []

      fp, s, d, f, pos, key, trap = a_star(g, a, game.g_pos)

      while src.parent is not None:
        print('------------------------ boy has parent ---------------------------------')
        print('child: ', src.pos)
        print('parent: ', src.parent.pos)
        print(src.path)

        #solution.append(src.path[-1][::-1])
        solution.append(src.path)
        src = src.parent

      solution.reverse()
      solution.append(fp[1:])
      print()
      for i in solution:
        print(i)
      print(len(solution))
      print('********** solution final *****')

      return solution

    current = copy.deepcopy(src)
    current.childs = goals

    print('visitados ', current.visited)
    if goals[idx].pos not in current.visited or len(goals) == 1:
      print('############ src: ', a.pos, ' ###############')
      print('############ end: ', goals[idx].pos, goals[idx].h, ' ###############')
      path, g.state, g.diamonds, g.finish, a.pos, a.has_key, trap = a_star(g, a, goals[idx].pos)
      print()
      print('src with ', src.pos, src.h)
      print('a.pos with ', a.pos)
      print('path with ', goals[idx].pos, goals[idx].h)
#      print(path)
      print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
      
      if len(path) > 0:
#        visited.add(goals[idx].pos)
        
        temp = copy.deepcopy(goals[idx])
        temp.agent = a
        temp.game = g
        temp.trap = trap
        src.visited.add(goals[idx].pos)
        temp.visited = src.visited

        print(count, ' idx ', idx , 'src ', src.pos, ' kid ', temp.pos)
        temp.parent = current 

        new_order = get_goals(temp.agent, temp.game)
        temp.path = path[1:]
#        print(temp.pos, temp.path)

        return make_path(temp.agent, temp.game, temp, new_order)

      else:
#        visited.add(goals[idx].pos)
        current.visited.add(goals[idx].pos)
#        current.childs.remove(goals[idx])
        print('else case:')
        print(current.visited)
        if len(goals) > 1 and goals[idx+1].pos:# not in current.visited:
          print('*********************************** SWAP ***********************************')
          print(goals[idx].pos, goals[idx+1].pos)

          goals = goals[idx+1:] + [goals[idx]]
          goals = copy.deepcopy(goals)
#          make_path(a, g, goals[idx], goals)
          return make_path(current.agent, current.game, current, goals)
        else:
          print('%%%%%%%%%%%%%%%%%% backtrack parent %%%%%%%%%%%%%%%%%%%')
          if current.parent:
            print('child: ', current.pos, ' parent: ', current.parent.pos)
          
          while current.parent:
            print('child: ', current.pos, ' parent: ', current.parent.pos)
            if current.trap and current.parent.pos not in visited_trap:
              print(current.pos)
              break
            current.visited = set()
            current = current.parent

          print('it breaks ok')
          if current.parent and current.parent.pos not in visited_trap:
            print(' child visited: ', current.visited)
            print(' parent visited ', current.parent.visited)
            current.visited = set()
            current = current.parent

          visited_trap.add(current.pos)
#      goals = get_goals(current.agent, current.game)
          current.childs = current.childs[idx+1:] + [current.childs[idx]]
          for i in current.childs:
            print(i.pos, i.h)
          print('$$$$$$$$$$$$$$$$$$$$$$4 order after backtracking ###########################3')
          return make_path(current.agent, current.game, current, current.childs, visited_trap)
    else:
      print('%%%%%%%%%%%%%%%%%% backtrack parent %%%%%%%%%%%%%%%%%%%')
      if current.parent:
        print('child: ', current.pos, ' parent: ', current.parent.pos)
      
      while current.parent:
        print('child: ', current.pos, ' parent: ', current.parent.pos)
        if current.trap and current.parent.pos not in visited_trap:
          print(current.pos)
          break
        current.visited = set()
        current = current.parent

      print('it breaks ok')
      if current.parent and current.parent.pos not in visited_trap:
        print(' child visited: ', current.visited)
        print(' parent visited ', current.parent.visited)
        current.visited = set()
        current = current.parent

      visited_trap.add(current.pos)
#      goals = get_goals(current.agent, current.game)
      current.childs = current.childs[idx+1:] + [current.childs[idx]]
      for i in current.childs:
        print(i.pos, i.h)
      print('$$$$$$$$$$$$$$$$$$$$$$4 order after backtracking ###########################3')
      return make_path(current.agent, current.game, current, current.childs, visited_trap)

    return []

  return solution

def solver(game, agent) :
  a = copy.deepcopy(agent)
  g = copy.deepcopy(game)
  
  src = Goal(a.pos, 0, 'i', a , g) 

  solution = []

  goals = get_goals(a, g)
  solution = make_path(a, g, src, goals)
  print(len(solution))
  moves = []

  print()
  print()
  print('final len ',len(solution))
  for i in solution:
    for j in i:
      print(j[0])
      moves.append(j[0])
#  print('moves len: ', len(moves))
#  sys.exit('die')
  return moves 

