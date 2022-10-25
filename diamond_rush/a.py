#!/usr/bin/python3
from enviroment import s, fs
from heapq import heappush, heappop

class Node():
  def __init__(self, pos=None, parent=None, visited=False):
    self.pos = pos
    self.parent = parent
    self.visited = visited

    self.g = 0
    self.h = 0
    self.f = self.g + self.h

  def h(self, h):
    self.h = h

  def g(self, g):
    self.g = g

  def f(self):
    return self.h + self.g

  def __eq__(self, other):
    return self.pos == other.pos
    #return self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]

def back_trace():
  pass

def get_neighbors(node):
  neighbors = []
  for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
    n = Node((node.pos[0] + i[0], node.pos[1] + i[1]))
    neighbors.append(n)
  return neighbors

def a_star(grid, src, dest):
  src_node = Node(src)
  dest_node = Node(dest)
  print(src_node.h)
  print(dest_node.g)

  open_list = []
  came_from = []
#  open_list.append(src_node)
# use min heap instead
  heappush(open_list, src_node)
  src_node.visited = True
  
  while open_list:
    current = heappop(open_list)

    if current == dest_node:
# TODO: backtrace path
      return

    neighbors = get_neighbors(current)

    for n in neighbors:
      if n.visited:
        continue
      pos  = n.pos
      
    print(current.pos)
    break

def main():
  src = (5, 2)
  dest = (12,7)
  print(s)
  path = a_star(s, src, dest)

if __name__ == '__main__':
    main()
