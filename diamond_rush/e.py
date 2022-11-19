#!/usr/bin/env python3
import numpy as np

# How to optimize with this 
from heapq import heappush, heappop

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

def a_star(grid, start, end):

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
              print('current node: ', current.pos)
              path.append(current.pos)
              current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        print('current node position: ', current_node.pos)

        ### Replace for possible_actions in game.py
        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            ### No need of this with possible_actions in game.py
            # Get node pos
            node_pos = (current_node.pos[0] + new_pos[0], current_node.pos[1] + new_pos[1])
            
            ### No need of this with possible_actions in game.py
            # Make sure within range
            if node_pos[0] > (len(grid) - 1) or node_pos[0] < 0 or node_pos[1] > (len(grid[len(grid)-1]) -1) or node_pos[1] < 0:
                continue

            ### No need of this with possible_actions in game.py
            # Make sure walkable terrain
            if grid[node_pos[0]][node_pos[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_pos)

            # Append
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


def main():

    maze = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (0,1)
#    end = (9, 5)

    path = a_star(maze, start, end)
    print(path)

if __name__ == '__main__':
    main()
