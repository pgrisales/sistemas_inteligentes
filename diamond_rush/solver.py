#!/usr/bin/env python3
import copy
from a_star import a_star
from game import buttons_pos, holes_pos, keys_pos, rocks_pos, kDoor_pos
import sys

class Goal:
  def __init__(self, pos, h, type_char, agent=None, game=None, parent=None, childs=[], visited= set(), rocks=[]):
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
    if self.game:
      self.rocks = rocks_pos(self.game.state)
#    self.n_rock = n_r(self.pos, rocks_pos(self.game.state))

  def n_rock(self, pos, rocks):
    return n_r(pos, rocks)

  def __eq__(self, other):
    return self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]

  def __lt__(self, other):
    return self.h < other.h

def n_r(goal, r_pos):
  nearest = r_pos[0]
  for i in range(1, len(r_pos)):
    if h(goal, r_pos[i]) < h(goal, nearest):
      nearest = r_pos[i]

  return nearest

def order_goals(childs, agent,r):
  childs = set_priority(agent,r,childs)
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

def set_goals_holes(pos, holes, a, g):
  goals = []
  for idx, i in enumerate(holes):
    new_h = h(pos, i)
    nd = Goal(i, new_h, 'h', a, g)
    goals.append(nd)
    for j in range(idx):
      if goals[idx].h < goals[j].h:
        goals[idx], goals[j] = goals[j], goals[idx]
  
  return goals

def set_goals_keys(pos, keys, a, g):
  goals = []
  for idx, i in enumerate(keys):
    new_h = h(pos, i)
    nd = Goal(i, new_h, 'k', a, g)
    goals.append(nd)
    for j in range(idx):
      if goals[idx].h < goals[j].h:
        goals[idx], goals[j] = goals[j], goals[idx]
  
  return goals

def set_goals_buttons(pos, buttons, a, g):
  goals = []
  for idx, i in enumerate(buttons):
    new_h = h(pos, i)
    nd = Goal(i, new_h, 'b', a, g)
    goals.append(nd)
    for j in range(idx):
      if goals[idx].h < goals[j].h:
        goals[idx], goals[j] = goals[j], goals[idx]
  
  return goals

def set_goals_diamonds(pos, diamonds, a, g):
  goals = []
  for idx, i in enumerate(diamonds):
    new_h = h(pos, i)
    nd = Goal(i, new_h, 'd', a, g)
    goals.append(nd)
    for j in range(idx):
      if goals[idx].h < goals[j].h:
        goals[idx], goals[j] = goals[j], goals[idx]
  
  return goals

def set_goals_kDoors(pos, diamonds, a, g):
  goals = []
  for idx, i in enumerate(diamonds):
    new_h = h(pos, i)
    nd = Goal(i, new_h, 'K', a, g)
    goals.append(nd)
    for j in range(idx):
      if goals[idx].h < goals[j].h:
        goals[idx], goals[j] = goals[j], goals[idx]
  
  return goals

def set_priority(agent,r, *args):
  goals = []
  for goal in args:
    for idx, i in enumerate(goal):
      goals.append(i)

      if i.type == 'd':
        i.h += h(agent.pos, i.pos) + i.h2
      elif i.type == 'k':
        i.h += h(agent.pos, i.pos) + i.h2
      elif i.type == 'b':
        i.h += h(agent.pos, i.pos) + i.h2 + 8
      elif i.type == 'h':
        i.h += h(agent.pos, i.pos) + i.h2 
      elif i.type == 'K':
        i.h += h(agent.pos, i.pos) + i.h2 
  if r:
    goals.sort(key=lambda x: x.h, reverse=True)          
  else:
    goals.sort(key=lambda x: x.h)          

  return goals

def get_goals(a, g, r=False):
  diamonds= set_goals_diamonds(a.pos, g.diamonds, a, g)
  keys = set_goals_keys(a.pos, keys_pos(g.state), a, g)
  holes = set_goals_holes(a.pos, holes_pos(g.state), a, g)
  buttons = set_goals_buttons(a.pos, buttons_pos(g.state), a, g)
  kdoors = set_goals_kDoors(a.pos, kDoor_pos(g.state), a, g)
#  rocks = rocks_pos(g.state) # Not sure its needed here

  goals = set_priority(a,r, diamonds, keys, holes, buttons, kdoors)
  goals = order_goals(goals, a, r)
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
  
  print()
  for z in goals:
    print(z.pos, z.h, z.type, '    a.key: ', agent.has_key)
  print('---------------------- still to getem --------------------------------')

  while not g.finish:
    if len(goals) == 0:
      solution = []
      f_goal = Goal(game.g_pos, 0, 'g')
      fp, s, d, f, pos, key, trap = a_star(g, a, f_goal)

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
#    current.childs = order_goals(current.childs, current.agent,False)

    print('visitados ', current.visited)
    if goals[idx].pos not in current.visited or len(goals) == 1:
      print('############ src: ', a.pos, ' ###############')
      print('############ end: ', goals[idx].pos, goals[idx].h, goals[idx].type, ' ###############')
      path, g.state, g.diamonds, g.finish, a.pos, a.has_key, trap = a_star(g, a, goals[idx])

      print()
      print('src with ', src.pos, src.h, 'is trap: ', src.trap)
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
        if goals[idx].type == 'r' or goals[idx].type == 'b':
          goals[idx].rocks.pop(0)

        print('else case:')
        print(current.visited)
        if len(goals) > 1 and goals[idx+1].pos:# not in current.visited:
          print('*********************************** SWAP ***********************************')
          print(goals[idx].pos, goals[idx+1].pos)

          goals = goals[idx+1:] + [goals[idx]]
          return make_path(current.agent, current.game, current, goals)
#          return make_path(current.agent, current.game, current, current.childs)
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
          current.childs = current.childs[idx+1:] + [current.childs[idx]]
          current.childs = order_goals(current.childs, current.agent,True)
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
      goals = get_goals(current.agent, current.game,True)
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

