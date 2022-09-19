#!/usr/bin/env python3
from states import m,m2
from random import randint
# muro = m
# agent = a
# path = p
# diamond = d
# spikes = s
# goal = g

# movements: r,l,u,d
# rules -> all d,

def isValid(i,j):
  if i < 0 or i > 10 or j < 0 or j > 8:
    return 1
  return 0

movs = []
def move():
  des = randint(0,4)
  if des == 0:
    return

def solve():
  while m != m2:
    move()
  print(movs)

solve(m,m2)
print(m)
print('**********************************************')
print(m2)


