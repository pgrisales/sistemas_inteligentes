#!/usr/bin/env python3
# How to optimize with this? 
#from heapq import heappush, heappop

# Diamond heuristic
def h_d(src, goal):
  pass

# Sokoban type heuristic
def h_r(src, goal):
  pass
  
# Manhattan heuristic
def h(src, goal):
  return abs(src.pos[0] - goal.pos[0]) +  abs(src.pos[1] - goal.pos[1])  

class Node():

  def __init__(self, parent=None, pos=None):
    self.parent = parent
    self.pos = pos

    self.g = 0
    self.h = 0
    self.f = 0

  def __eq__(self, other):
    return self.pos == other.pos

def a_star(game, agent, end):

  start = agent.pos
  print(agent.pos)
  # Create start and end node
  start_node = Node(None, start)
  start_node.g = start_node.h = start_node.f = 0
  end_node = Node(None, end)
  end_node.g = end_node.h = end_node.f = 0

  # Initialize both open and closed list
  open_list = []
  closed_list = []

  # Add the start node
  open_list.append(start_node)

  # Loop until you find the end
  while len(open_list) > 0:

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

    # Found the goal
    if current_node == end_node:
      path = []
      current = current_node
      while current is not None:
#        print('current node: ', current.pos)
        path.append(current.pos)
        current = current.parent
      return path[::-1] # Return reversed path

    # Generate children
    children = []

    agent.pos = current_node.pos
    print(agent.pos)
#    print(game.state)
    # Possible actions
    new_pos = game.possible_actions(agent, game)
    for k, v in new_pos.items():
#      print('childs: ', v())
      new_node = Node(current_node, v())
      children.append(new_node)

    # Loop through children
    for child in children:

      # Child is on the closed list
      for closed_child in closed_list:
        if child == closed_child:
          continue
#            print('current node: ', current_node.pos)

      # Create the f, g, and h values
      child.g = current_node.g + 1
      child.h = h(child, end_node)
      print(child.pos, child.h)
      child.f = child.g + child.h

      # Child is already in the open list
      for open_node in open_list:
        if child == open_node and child.g > open_node.g:
          continue

      # Add the child to the open list
      open_list.append(child)

