#!/usr/bin/env python3
from itertools import permutations
import random

DIGITS = '0123456789'

def noDuplicates(num):
  if len(num) == len(set(num)):
    return True
  else:
    return False

def genNum():
    while True:
      num = ''
      for i in range(4):
        num = ''.join([num, str(random.randint(0,9))])
      if noDuplicates(num):
        return num

def NoBulls_cows(num, guess):
  bulls = 0; cows = 0;
  #loop to count number of bulls and cows
  for i in guess:
    if i in num:
      if (guess.index(i) == num.index(i)):
        bulls += 1
      else:
        cows += 1
  fijas = str(bulls)
  picas = str(cows)
  pf = ','.join([picas,fijas])
  return pf

def enviroment():
  c = input()
  if c == 'S':
    let_guess()
  elif c == 'R':
    guess()

def let_guess():
  win = False
  while not win:
    c = input()

    if c == '#':
      num = genNum()
      print(num)
    elif len(c) == 4:
      guess = c
      bulls_cows = NoBulls_cows(num,guess)
      print(bulls_cows)
      print(bulls_cows[2])
      if bulls_cows[2] == '4':
        win = True

def guess():
  perms = list(permutations(DIGITS, 4))
  guesses = []
  hits  = []

  while True:
      guess = perms[0]
      guesses.append(guess)
      g = ''.join(guess)
      print("El numero es: ", g, "?")
      bulls_cows = list(input().split(','))
      hit = [int(bulls_cows[0]),int(bulls_cows[1])]
      hits.append(hit)
      if (hit == [4, 0]):
          print ("ENCONTRADO")
          print("El numero es: ", g)
          break

# perms2 is a filter permutations options
      perms2 = []
      print(perms2)
      for p in perms:
        print(len(perms))
        if (NoBulls_cows(p,guess) == hit):
          perms2.append(p)
      perms = perms2

      if not perms:
          print ("Hay algo mal en las respuestas:")
          break
if __name__ == '__main__':
  while True:
    enviroment()

