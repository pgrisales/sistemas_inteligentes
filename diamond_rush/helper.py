#!/usr/bin/env python3
from pynput.keyboard import Key, Controller
import time

kb = Controller()

time.sleep(3)

def move(key):
  kb.press(key)
  time.sleep(0.15)
  kb.release(key)
  time.sleep(0.15)
  
def play(moves):
  for d in moves:
    if d == 'l':
      move(Key.left)
    elif d == 'r':
      move(Key.right)
    elif d == 'u':
      move(Key.up)
    elif d == 'd':
      move(Key.down)

l10 = 'ulrrdllddrdrrurddrruudddduullrlullllddddrrrrlrllllddrrrruuurrurldlldddrrrllluuuurdruuuuddlldddrlddrruuuuuuuuulll'
l11 = 'lrrrdrrudrddddddduulrddlruullddrdllluuullldddrrruuulluuulrurrdrrrrdddddd'
play(l11)
