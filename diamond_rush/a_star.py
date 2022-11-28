#!/usr/bin/env python3
# How to optimize with this? 
#from heapq import heappush, heappop
from rules import rules, possible_actions

import sys
import copy
# Diamond heuristic
def h_d(src, goal):
  pass

# Sokoban type heuristic
def h_r(src, goal):
  pass
  
# Manhattan heuristic
def h(src, goal):
  return abs(src.pos[0] - goal.pos[0]) +  abs(src.pos[1] - goal.pos[1])  

# possible_actions(state, level, diamonds, finish, a_pos, key)
class Node():
  def __init__(self, parent=None, pos=None, 
              direction=None, state=None,
              level=None, goal=None,
              diamonds=None, finish=None, key=None):
    self.parent = parent
    self.pos = pos

    self.direction = direction
    self.state = state
    self.level = level
    self.goal = goal
    self.diamonds = diamonds
    self.finish = finish
    self.key = key

    self.g = 0
    self.h = 0
    self.f = 0
  
  def get_childs(self):
    pa = possible_actions(self.state, self.level, self.goal, self.diamonds, self.finish, self.pos, self.key)
    childs = []
    for k, v in pa.items():
      child = Node(self, v[1], k, v[0], self.level, self.goal, v[2], v[3], v[4])

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

  # Create start and end node
  start_node = Node(None, start, None, s, l, g, d, finish, k)
  start_node.g = start_node.h = start_node.f = 0
  end_node = Node(None, end)
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
    if count == 150:
      #print('shit case')
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
#      print('Good case')
      return path[::-1], t.state, t.diamonds, t.finish, t.pos, t.key, trap

    # Generate children
    children = []

    agent.pos = current_node.pos

    # Get childs
    childs = current_node.get_childs()
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
