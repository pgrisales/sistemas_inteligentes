#!/usr/bin/env python3
from rules import rules, possible_actions
import sys
import copy
from game import rocks_pos

# Sokoban type heuristic
def h_s(goal, n_rock):
  return abs(n_rock[0] - goal[0]) +  abs(n_rock[1] - goal[1])  
  
# Manhattan heuristic
def h(src, goal):
  return abs(src.pos[0] - goal.pos[0]) +  abs(src.pos[1] - goal.pos[1])  

# possible_actions(state, level, diamonds, finish, a_pos, key)
class Node():
  def __init__(self, parent=None, pos=None, 
              direction=None, state=None,
              level=None, goal=None,
              diamonds=None, finish=None, key=None, trap=None):
    self.parent = parent
    self.pos = pos

    self.direction = direction
    self.state = state
    self.level = level
    self.goal = goal
    self.diamonds = diamonds
    self.finish = finish
    self.key = key
    self.trap = trap

    self.g = 0
    self.h = 0
    self.f = 0
  
  def get_childs(self):
    pa = possible_actions(self.state, self.level, self.goal, self.diamonds, self.finish, self.pos, self.key)
    childs = []
    for k, v in pa.items():
      child = Node(self, v[1], k, v[0], self.level, self.goal, v[2], v[3], v[4], v[5])

      childs.append(child)
    return childs 

  def __eq__(self, other):
    return self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]

def a_star(o_g, o_a, end):

  agent = copy.deepcopy(o_a)
  game = copy.deepcopy(o_g)

  k =  agent.has_key
  s = game.state
  d = game.diamonds
  finish = game.finish
  g = game.g_pos
  l = game.level
  start = agent.pos
  g_type = end.type
  if end.type == 'h' or end.type == 'b':
    n_rock = end.n_rock(end.pos, end.rocks)
#  n_rock = end.n_rock

  # Create start and end node
  start_node = Node(None, start, None, s, l, g, d, finish, k)
  start_node.g = start_node.h = start_node.f = 0
  end_node = Node(None, end.pos)
  end_node.g = end_node.h = end_node.f = 0

  # Initialize both open and closed list
  open_list = []
  closed_list = []

  # Add the start node
  open_list.append(start_node)
  count = 0
  # Loop until you find the end
  while len(open_list) > 0:
    count += 1
#    if count == 150:
#    if count == 1550:
#    if count == 150:
    if count == 250:
      print('shit case')
      return [], o_g.state, o_g.diamonds, o_g.finish, o_a.pos, o_a.has_key, False 
    # Get the current node
    current_node = open_list[0]
    current_index = 0
    for index, item in enumerate(open_list):
      if item.f < current_node.f:
        current_node = item
        current_index = index

    # Pop current off open list, add to closed list
    open_list.pop(current_index)
    closed_list.append(current_node)


    if g_type == 'h' or g_type == 'b':

      if current_node.state[end_node.pos[0], end_node.pos[1]] == 'p':
        if end_node.pos == (12,3) or end_node.pos == (11,6):
          print(end_node.pos)
          print('----------------------------- shit working ------------------------------------')
#          sys.exit('terminando hole')
        trap = False
        path = []
        current = current_node
        t = current_node
        while current is not None:
          path.append([current.direction, current.pos])
          if current.parent is not None:
            past = current.parent.state[current.pos[0], current.pos[1]]

            if past == 'r' or past == 's' or past == 'R':
              trap = True

          current = current.parent
        return path[::-1], t.state, t.diamonds, t.finish, t.pos, t.key, trap
    else:
      # Goal found
      # Fix tuple and list output -> use just one
      if current_node == end_node:
        trap = False
        path = []
        current = current_node
        t = current_node
        while current is not None:
#        print('current node: ', current.pos)
          path.append([current.direction, current.pos])
          if current.parent is not None:
            past = current.parent.state[current.pos[0], current.pos[1]]

            if past == 'r' or past == 's' or past == 'R':
              trap = True

          current = current.parent
        # reversed path
        return path[::-1], t.state, t.diamonds, t.finish, t.pos, t.key, trap

    # Generate children
    children = []

    agent.pos = current_node.pos

    # Get childs
    childs = current_node.get_childs()
#    if current_node.h == 1:
#      for i in childs:
#        print(child.pos, child.h)
#        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    for i in childs:
      children.append(i)

    # Loop through children
    for child in children:

      # Child is on the closed list
      for closed_child in closed_list:
        if child == closed_child:
          continue
#            print('current node: ', current_node.pos)
#      if child.parent.state[child.pos[0], child.pos[1]] == 'd':
#        print('#################################')
#        print('DIAMANDA ADJACENTE')
#        child.g -= 1

      # Create the f, g, and h values
      child.g = current_node.g + 1
      if g_type == 'h' or g_type == 'b':
        if child.state[end.pos] == 'p':
          child.h = 0
        else:
          n_rock = end.n_rock(end.pos, rocks_pos(child.state))
          child.h = h_s(end.pos, n_rock) + rock_trap(child.state, n_rock, end)# + h_s(child.pos, n_rock)
          if child.parent.state[n_rock] == 'r':
            child.h += 1

#          if child.pos not in [ (n_rock[0]-1, n_rock[1]), (n_rock[0]+1, n_rock[1]), (n_rock[0], n_rock[1]-1), (n_rock[0], n_rock[1]+1)]:
          if end.pos[0] < n_rock[0]:
            child.h += h_s(child.pos, (n_rock[0]+1, n_rock[1]))
          elif end.pos[0] > n_rock[0]:
            child.h += h_s(child.pos, (n_rock[0]-1, n_rock[1]))
          elif end.pos[1] < n_rock[1]:
            child.h += h_s(child.pos, (n_rock[0], n_rock[1]+1))
          elif end.pos[1] > n_rock[1]:
            child.h += h_s(child.pos, (n_rock[0], n_rock[1]-1))

#        if end.pos == (12,3):
        if child.h < 2:
          print(child.state)
          print(child.pos, child.h)
          print()
          print('rock: ', n_rock, 'end pos: ', end.pos)
          hpta = child.get_childs()
          print()
          for i in hpta:
            print(i.pos, i.h)
          print('----------------- possible kids -----------------')
      else:
        child.h = h(child, end_node)
      #print(child.state)
      #print(child.pos, child.h)
      child.f = child.g + child.h

# Test incentiva ir hacia diamante cerca en el camino, parece que funciona en el level 2
#      if child.parent.state[child.pos[0], child.pos[1]] == 'd':
#        print('#################################')
#        print('DIAMANDA ADJACENTE')
#        child.g -= 1

      # Child is already in the open list
      for open_node in open_list:
        if child == open_node and child.g > open_node.g:
          # Pa no incentivar la busqueda en nodos ya visitados
          open_node.g += 1
          continue

      # Add the child to the open list
      open_list.append(child)

def rock_trap(state, rock, end):
  count = 0
  if rock[0] == end.pos[0] and rock[1] == end.pos[1]:
    return 0
  else:
    if state[rock[0]-1, rock[1]] == 'w' or state[rock[0]+1, rock[1]] == 'w':
      count += 1
    if state[rock[0], rock[1]-1] == 'w' or state[rock[0], rock[1]+1] == 'w':
      count += 1
    if count == 2:
      return 1
  return 0
