#!/usr/bin/env python3
from enviroment import Env
from browser import Browser
import sys

def main():
  pass

if __name__ == "__main__":

  if len(sys.argv) > 1:
    assert sys.argv[1].isdigit(), "Invalid input"

    level = int(sys.argv[1]) 

    assert level in range(1, 21), "Invalid level"

    env = Env(level)
    env.test()

  else:
    main()
