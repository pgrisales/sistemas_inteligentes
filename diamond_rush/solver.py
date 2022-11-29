#!/usr/bin/env python3
import copy
from a_star import a_star
from game import buttons_pos, holes_pos, keys_pos, rocks_pos, kDoor_pos
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

  def __lt__(self, other):
    return self.h < other.h

def order_goals(childs, agent):
  childs = set_priority(agent,childs)
  if agent.has_key:
    a = [] 
    b = []
    idx = 0
    while childs:
      if childs[idx].type == 'k':
        b.append(childs.pop(idx))
      else:
        a.append(childs.pop(idx))

    for i in b:
      a.append(i)

    return a
  else:
    a = [] 
    b = []
    idx = 0
    while childs:
      if childs[idx].type == 'K':
        b.append(childs.pop(idx))
      else:
        a.append(childs.pop(idx))

    for i in b:
      a.append(i)

    return a
# Alternate diamond-key Order
#    for idx in range(childs-2):
#      if childs[idx] == 'k' and childs[idx+1] == 'k': 
#        childs = childs
#  print('###########################################################################################')
#  print('new len: ', len(childs))
  return childs

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

def set_goals_kDoors(pos, diamonds):
  goals = []
  for idx, i in enumerate(diamonds):
    new_h = h(pos, i)
    nd = Goal(i, new_h, 'K')
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
#        if agent.has_key:
#          i.h += 10
      elif i.type == 'b':
        i.h += h(agent.pos, i.pos) + i.h2 + 8
      elif i.type == 'h':
        i.h += h(agent.pos, i.pos) + i.h2 + 8
      elif i.type == 'K':
        i.h += h(agent.pos, i.pos) + i.h2 
#        i.h += h(agent.pos, i.pos) + i.h2 + 10
  goals.sort(key=lambda x: x.h)          

  return goals

def get_goals(a, g):
  diamonds= set_goals_diamonds(a.pos, g.diamonds)
  keys = set_goals_keys(a.pos, keys_pos(g.state))
  holes = set_goals_holes(a.pos, holes_pos(g.state))
  buttons = set_goals_buttons(a.pos, buttons_pos(g.state))
  kdoors = set_goals_kDoors(a.pos, kDoor_pos(g.state))
#  rocks = rocks_pos(g.state) # Not sure its needed here

  goals = set_priority(a, diamonds, keys, holes, buttons, kdoors)
#  goals = set_priority(a, diamonds, keys, holes, buttons)
  goals = order_goals(goals, a)
  return goals

count = 0
def make_path(agent, game, src, goals, visited_trap=set()):
  global count
  count += 1
  print(count)
  a = agent
  g = game

  solution = []
  idx = 0
  if count == 40:
    sys.exit('outcount')
  
#  goals = copy.deepcopy(goals)

  print()
  for z in goals:
    print(z.pos, z.h, z.type, '    a.key: ', agent.has_key)
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

        solution.append(src.path)
        src = src.parent

      solution.reverse()
      solution.append(fp[1:])
#      print()
#      for i in solution:
#        print(i)
#      print(len(solution))
#      print('********** solution final *****')

      return solution

    current = copy.deepcopy(src)
    current.childs = goals
    current.childs = order_goals(current.childs, current.agent)

    print('visitados ', current.visited)
    if goals[idx].pos not in current.visited or len(goals) == 1:
      print('############ src: ', a.pos, ' ###############')
      print('############ end: ', goals[idx].pos, goals[idx].h, goals[idx].type, ' ###############')
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
#        temp.visited = src.visited
        temp.visited = set()
        print(count, ' idx ', idx , 'src ', src.pos, ' kid ', temp.pos)
        temp.parent = current 

        new_order = get_goals(temp.agent, temp.game)
#        new_order = order_goals(new_order, temp.agent)

        temp.path = path[1:]
#        print(temp.pos, temp.path)

        return make_path(temp.agent, temp.game, temp, new_order)

      else:
        current.visited.add(goals[idx].pos)

        print('else case:')
        print(current.visited)
        if len(goals) > 1 and goals[idx+1].pos:# not in current.visited:
          print('*********************************** SWAP ***********************************')
          print(goals[idx].pos, goals[idx+1].pos)

          goals = goals[idx+1:] + [goals[idx]]
          return make_path(current.agent, current.game, current, goals)
#          return make_path(current.agent, current.game, current, current.childs)
        else:
          while current.parent:
            if current.trap and current.parent.pos not in visited_trap:
              break
            current.visited = set()
            current = current.parent

          if current.parent and current.parent.pos not in visited_trap:
            #print(' child visited: ', current.visited)
            #print(' parent visited ', current.parent.visited)
            current.visited = set()
            current = current.parent

          visited_trap.add(current.pos)
          current.childs = current.childs[idx+1:] + [current.childs[idx]]
          current.childs = order_goals(current.childs, current.agent)
          for i in current.childs:
            print(i.pos, i.h, i.type)
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
      goals = get_goals(current.agent, current.game)
#      current.childs = order_goals(current.childs, current.agent)
      for i in current.childs:
        print(i.pos, i.h, i.type)
      print('$$$$$$$$$$$$$$$$$$$$$$4 order after backtracking ###########################3')
      return make_path(current.agent, current.game, current, current.childs, visited_trap)

    return []

  return solution

def solver(game, agent) :
  
  src = Goal(agent.pos, 0, 'i', agent, game) 

  solution = []

  goals = get_goals(agent, game)
  for i in goals:
    print(i.pos, i.h, i.type)

  solution = make_path(agent, game, src, goals)
  print(len(solution))
  moves = []

  print()
  print()
  print('final len ',len(solution))
  for i in solution:
    for j in i:
      print(j[0])
      moves.append(j[0])

  return moves 

