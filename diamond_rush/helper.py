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
  
def play(d):
  if d == 'l':
    print('l')
    move(Key.left)
  elif d == 'r':
    print('r')
    move(Key.right)
  elif d == 'u':
    print('u')
    move(Key.up)
  elif d == 'd':
    print('d')
    move(Key.down)

l0 = 'rrrrrdddlllllddrdrrrrd'
for i in l0: 
  play(i)


